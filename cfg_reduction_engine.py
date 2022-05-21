from cfg_validation_engine import ContextFreeGrammar

if __name__ == '__main__':
    CFG = ContextFreeGrammar("cfg_config_file")
    CFG.UselessReduction()
    CFG.NullReduction()
    CFG.UnitReduction()
    CFG.PrintContextFreeGrammar()