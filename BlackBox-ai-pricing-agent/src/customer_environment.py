# src/firm_pricing_competition/customer_environment.py

from __future__ import annotations

from typing import Iterable, Tuple, List, Optional
import numpy as np


# ============================================================
# A BİLGİLERİ (DEĞİŞTİRİLMEZ SABİTLER)
# ============================================================
CUSTOMERS: int = 1000

# Customer distribution parameters
AGE_MEAN: float = 25
AGE_STD: float = 5
INCOME_MEAN: float = 30
INCOME_STD: float = 8

# Reference (centering) values
REF_PRICE: float = 50
REF_AGE: float = 25
REF_INCOME: float = 40

# Utility function coefficients
BETA_PRICE: float = -0.1
BETA_AGE: float = -0.01
BETA_INCOME: float = 0.05


# ============================================================
# POPÜLASYON ÜRETİMİ / KAYDET-YÜKLE  (NEMIDE: KORUNACAK)
# ============================================================
def generate_population(seed: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    A bilgilerine göre popülasyon yalnızca run başında 1 kez üretilir.
    Bu fonksiyon ages ve incomes vektörlerini döndürür.

    Not: Reprodüksiyon için Nemide'nin default_rng + seed yaklaşımı KORUNUR.
    """
    rng = np.random.default_rng(seed)
    ages = rng.normal(AGE_MEAN, AGE_STD, CUSTOMERS).astype(float)
    incomes = rng.normal(INCOME_MEAN, INCOME_STD, CUSTOMERS).astype(float)
    return ages, incomes


def save_population(path_npz: str, ages: np.ndarray, incomes: np.ndarray) -> None:
    """
    Popülasyonu output klasörüne kaydetmek için.
    (Nemide davranışı: KORUNUR)
    """
    np.savez(path_npz, ages=np.asarray(ages, dtype=float), incomes=np.asarray(incomes, dtype=float))


def load_population(path_npz: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Popülasyonu output klasöründen yüklemek için.
    (Nemide davranışı: KORUNUR)
    """
    data = np.load(path_npz)
    ages = np.asarray(data["ages"], dtype=float)
    incomes = np.asarray(data["incomes"], dtype=float)
    return ages, incomes


# ============================================================
# SOFTMAX + CHOICE (DENIZ İLE AYNI HALE GETİRİLDİ)
# ============================================================
def softmax(utilities: np.ndarray) -> np.ndarray:
    """
    Deniz'in çalışmasındaki gibi (stabil olmayan) softmax:
      exp(U) / sum(exp(U))

    utilities shape: (CUSTOMERS, K)
    """
    exp_util = np.exp(utilities)
    return exp_util / exp_util.sum(axis=1, keepdims=True)


def simulate_tick_sales(
    prices: Iterable[float],
    ages: np.ndarray,
    incomes: np.ndarray,
) -> Tuple[List[int], int]:
    """
    Deniz'in S0 koduyla aynı talep/satış simülasyonu.

    - Utility matrisi: (CUSTOMERS, n_sellers+1)  (+1: no-buy)
    - U_{j,i} = BETA_PRICE*(p_i-REF_PRICE) + BETA_AGE*(age_j-REF_AGE) + BETA_INCOME*(income_j-REF_INCOME)
    - U_{j,no_buy} = 0
    - Probabilities: softmax(U)   (Deniz tarzı: stabilizasyon yok)
    - Sampling: Her müşteri için np.random.choice(..., p=...) (Deniz tarzı)
    - Sales: choices.count(i)
    - NoBuy: choices.count(n_sellers)

    Çıktı:
      - sales_by_firm: her firma için satış adedi (int)
      - no_buy: no-buy adedi (int)

    Not: Popülasyonun reprodüksiyon özelliği (save/load) bu fonksiyon tarafından değil,
    generate_population + save/load akışı tarafından korunur.
    """
    prices_list = list(prices)
    n_sellers = len(prices_list)
    if n_sellers < 1:
        raise ValueError("simulate_tick_sales: En az 1 satıcı olmalı.")

    # Deniz kodu varsayımsal olarak ages/incomes uzunluklarını kontrol etmiyor;
    # burada yalnızca bariz bozulmaları yakalamak için minimum kontrol bırakıyoruz.
    ages = np.asarray(ages, dtype=float)
    incomes = np.asarray(incomes, dtype=float)
    if ages.shape[0] != CUSTOMERS or incomes.shape[0] != CUSTOMERS:
        raise ValueError(f"simulate_tick_sales: ages/incomes uzunluğu CUSTOMERS={CUSTOMERS} olmalı.")

    # Utilities matrix
    utilities = np.zeros((CUSTOMERS, n_sellers + 1), dtype=float)  # +1 for no-buy

    # Deniz'in kod stiline birebir yakın: reduced_age ve reduced_income her i döngüsünde tekrar hesaplanır.
    for i in range(n_sellers):
        reduced_price = prices_list[i] - REF_PRICE
        reduced_age = ages - REF_AGE
        reduced_income = incomes - REF_INCOME
        utilities[:, i] = (
            BETA_PRICE * reduced_price
            + BETA_AGE * reduced_age
            + BETA_INCOME * reduced_income
        )

    # no-buy option utility
    utilities[:, -1] = 0.0

    # Probabilities
    probs = softmax(utilities)

    # Sampling (Deniz ile aynı yöntem)
    choices = [np.random.choice(n_sellers + 1, p=p) for p in probs]

    # Sales + no-buy counts (Deniz ile aynı)
    sales_by_firm = [choices.count(i) for i in range(n_sellers)]
    no_buy = choices.count(n_sellers)

    return sales_by_firm, no_buy
