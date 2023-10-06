#!/usr/bin/env python3
import rospy
from nlu_engine import NLU
from nlu.srv import NLUParsingService,NLUParsingServiceRequest,NLUParsingServiceResponse
from nlu.msg import Slot
from result_nlu import resultNLU

class node_nlu():

    def __init__(self) -> None:
        rospy.init_node('nlu_node')
        self.nlu = NLU()
        rospy.Service('nlu_parsing', NLUParsingService, self.callback_tts)
        self.current_changes = {}
        print("NLU Ready")


    def callback_tts(self,msg: NLUParsingServiceRequest):
        print("In callback:")
        self.nlu.setLanguage(msg.language)
        result : resultNLU = self.nlu.parse(msg.sentence)
        print(result)
        res = NLUParsingServiceResponse()
        res.intent = result.intent
        res.score = result.intent_proba
        res.slots = []
        for slot in result.slots:
            S = Slot()
            S.slotName = slot.slotName
            S.value = slot.value
            res.slots.append(S)
        return res

    # def swapOntoValues(self,old_value,new_value,language):
    #     print("change :",old_value," to : ",new_value)
    #     concept = self._onto.classes.find(old_value)
    #     type_concept = "classes"
    #     if(len(concept) == 0):
    #         print("search in individuals")
    #         concept = self._onto.individuals.find(old_value)
    #         type_concept = "individual"

    #     print(concept)
    #     if(len(concept)>=1):
    #         concept = concept[0]
    #         print("concept found : ",concept)
    #         if type_concept == "classes":
    #             old_names = self._onto.classes.getNames(concept)
    #         else:
    #             old_names = self._onto.individuals.getNames(concept)
    #         print("old_names : ",old_names)
    #         self._onto.feeder.waitConnected()
    #         for old_name in old_names:
    #             print("remove old name : ",old_name)
    #             self._onto.feeder.removeLanguage(concept,language,old_name)
    #         self.current_changes[concept] = {'old_values' : old_names ,'new_value' : new_value,'language':language}
    #         print(self.current_changes)
    #         self._onto.feeder.addLanguage(concept,language,new_value)
    #         self._onto.feeder.waitUpdate()
    #         print("end swap value")
    #     else:
    #         print("No concept found")

    # def resetOnto(self,data):
    #     print("Reset Onto to previous state")
    #     self._onto.feeder.waitConnected()
    #     for key,value in self.current_changes.items():
    #         self._onto.feeder.removeLanguage(key,value["language"],value["new_value"])
    #         for new in value["old_values"]:
    #             print("add : ",new)
    #             self._onto.feeder.addLanguage(key,value["language"],new)
    #     self._onto.feeder.waitUpdate()
    #     print("end reset onto")
    #     self.current_changes = {}
    #     # return EmptyResponse()

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = node_nlu()
    try:
        node.run()
    except rospy.ROSInterruptException:
        pass
