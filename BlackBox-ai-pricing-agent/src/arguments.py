import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument('--gui', dest='gui', action='store_true')
argparser.set_defaults(gui=False)

argparser.add_argument("--model_version", type=str, default='gemini-2.5-pro')
argparser.add_argument("--rounds", type=int, default=1000)
argparser.add_argument("--output_max_tokens", type=int, default=5000)  #128!!!
argparser.add_argument("--breakpoint_rounds", type=int, default=5000)
argparser.add_argument("--persona_firm1", type=int, default=1)
argparser.add_argument("--persona_firm2", type=int, default=1)
argparser.add_argument("--set_initial_price", dest='set_initial_price', action='store_true')
argparser.set_defaults(set_initial_price=True)

argparser.add_argument("--cost", type=int, default=[25,25], nargs=2)
argparser.add_argument("--initial_price", type=int, default=[25,25], nargs=2)
argparser.add_argument("--load_data_location", type=str, default='')

argparser.add_argument('--strategy', dest='strategy', action='store_true')
argparser.set_defaults(strategy=False)
argparser.add_argument('--has_conversation', dest='has_conversation', action='store_true')
argparser.set_defaults(has_conversation=False)
