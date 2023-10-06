from dataclasses import dataclass,field
from typing import List


@dataclass
class Slot():
    rawValue: str
    value: str
    slotName: str

    def __str__(self) -> str:
        msg = self.slotName + ' : '
        msg += self.value
        msg += " ("+self.rawValue+")"
        return msg


@dataclass
class resultNLU():
    input: str = ""
    intent: str = ""
    intent_proba : float =""
    slots: List[Slot] = field(default_factory=list)

    def __init__(self,dict_result):
        self.input = dict_result["input"]
        self.intent = dict_result["intent"]["intentName"]
        self.intent_proba = dict_result["intent"]["probability"]
        self.slots = []
        for slot in dict_result["slots"]:
            S = Slot(slot["rawValue"],slot["value"]["value"],slot["slotName"])
            self.slots.append[S]

    def __str__(self) -> str:
        msg = "Result :\n"
        msg += "Input : " + self.input + "\n"
        msg += "intent : " + self.intent + "\n"
        msg += "intent_proba : " + str(self.intent_proba) + "\n"
        msg += "slots : \n"
        for slot in self.slots:
            msg += "\t " + str(slot) + "\n"
        return msg
