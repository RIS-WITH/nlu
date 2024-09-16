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
        res.comprehension_score = result.intent_proba
        res.slots = []
        for slot in result.slots:
            S = Slot()
            S.slotName = slot.slotName
            S.value = slot.value
            res.slots.append(S)
        return res

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    node = node_nlu()
    try:
        node.run()
    except rospy.ROSInterruptException:
        pass
