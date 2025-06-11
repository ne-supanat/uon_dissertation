# TODO: few-shot
# TODO: chain of thought
# TODO: role-playing

# TODO: format
# TODO: negative prompt


class Prompt:
    def __init__(self, interview: str, topic: str, labelDict: dict[str, str]):
        self.interview = interview
        self.topic = topic
        self.labelDict = labelDict

    def name():
        return "default"

    def buildPrompt(self):
        return self.buildInstruction() + "\n\n" + self.buildFormat()

    def buildInstruction(self):
        return ""

    def buildFormat(self):
        return """Please response in this format.

"name": "Full name",
"age": "age number",
"occupation": "current occupation",
"key_memory": [
"supporting_evidence1",
"supporting_evidence2"
],
"domain_label": "domain_label"
"domain_label_reason": "domain_label_reason"
"""


class PromptZeroShot(Prompt):
    def name():
        return "zero-shot"

    def buildInstruction(self):
        return f"""Base on this interview.

{self.interview}

1. Extract following profile data:
- name
- age
- occupation

2. Find supporting evidence that related to {self.topic}

3. Based on the evidence what should be this profile label and why?
Pick a label from this list:
{'\n'.join([f"\"{key}\": {self.labelDict[key]}" for key in self.labelDict.keys()])}
"""


class PromptFewShot(Prompt):
    def name():
        return "few-shot"

    def buildInstruction(self):
        return f"""Base on this interview.

{self.interview}

1. Extract following profile data:
- name
- age
- occupation

Please response only with the answer. for example "name" from sentence such as "My name is John" the response is "John"
If there are no information present in the interview response with "None"

2. Find supporting evidence that related to {self.topic}

3. Based on the evidence what should be this profile label and why?
Pick a label from this list:
{'\n'.join([f"\"{key}\": {self.labelDict[key]}" for key in self.labelDict.keys()])}

Please response with only label for example {[f"\"{key}\": {self.labelDict[key]}" for key in self.labelDict.keys()][0]} the response is {[key for key in self.labelDict.keys()][0]} 
"""


# content = f"""Based on this interview.

#     {text}

#     extract interviewee data
#     1. personality
#     2. motivation
#     3. decision rules

#     give me a short answer
#     """

# content = f"""Based on this interview.

#     {text}

#     Where is the participant come from?
#     Please answer only name with sentence that tell the answer from original text.
#     For example, from sentence like "I'm from UK, Nottingham to be specific", please give a repsonse "UK, Nottingham // Evidence: I'm from UK, Nottingham to be specific"
#     """

# content = f"""You are a psychologist. Based on this interview.

#     {text}

#     Predict PHQ-8 score (0-24) with a short support evidence.
#     start with the evidence and end with a single score number e.g. 12.
#     """

# content = f"""Based on this interview.

#     {text}

#     Evaluate interviewee personality based on 4 emotion motivation aspects:
#     1. Care relates to relationships between individuals characterised by feelings of warmth and nurturance
#     2. Curiosity is the feeling of openness to exploration and having an effect on the environment
#     3. Cooperative is the positive affect that gives rise to engagement in goal-directed behaviour with others
#     4. Challenge is an aversive response to loss, whether actual or threatened, of valued resources, relationships, or knowledge, including self-beliefs

#     the scores are in range of 1-5
#     give each aspect a score and short evidence to support it.
#     """
