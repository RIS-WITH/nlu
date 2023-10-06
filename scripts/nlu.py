import argparse
import io
import json
import os, shutil
from result_nlu import resultNLU
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_FR,CONFIG_EN


class NLU:

    def __init__(self) -> None:
        self.engine = None
        self.current_language = ""
    
    def setLanguage(self,language= "fr",already_train = True):
        if language != self.current_language:
            self.current_language = language
            if language == "fr": 
                if already_train:
                    self.engine = SnipsNLUEngine.from_path("config/engine/fr_engine")
                else:
                    self.engine= SnipsNLUEngine(config=CONFIG_FR)
            elif language == "en":
                print('set to english')
                if already_train:
                    self.engine = SnipsNLUEngine.from_path("config/engine/en_engine")
                else:
                    self.engine= SnipsNLUEngine(config=CONFIG_EN)


    def train(self,path):
        if self.engine is None:
            print("Error first set the language to initialize the nlu engine")
            return
        with io.open(path) as f:
            dataset = json.load(f)
        self.engine.fit(dataset)
    
    def save_engine(self,path):
        if(os.path.isdir(path)):
            shutil.rmtree(path)
        if self.engine is None:
            print("Error first set the language to initialize the nlu engine")
            return
        self.engine.persist(path)
    

    def parse(self,text:str) -> resultNLU:
        if self.engine is None:
            print("Error first set the language to initialize the nlu engine")
            return
        return resultNLU(self.engine.parse(text))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="nlu script to lib and to train") #TODO add call to module for transform yaml to json
    parser.add_argument("--language","-l",dest='language',help="robot name",required=True)
    args = parser.parse_args()
    lang = args.language.lower()
    if(lang == "fr" or lang == "en"):
        print("Language is : ",lang)
        nlu = NLU()
        nlu.setLanguage(lang,False)
        print("---- Training ----")
        nlu.train(f'config/dataset/{lang}_dataset.json')
        print("---- Saving ----")
        nlu.save_engine(f"config/engine/{lang}_engine")
        print("---- End ---")
    else:
        print("Wrong language input try with en or fr")

