import llm


def extract_code_and_qoute(interview: str) -> str:
    prompt = f"""
Based on this transcript

{interview}

And the structure of Engineering Agent-Based Social Simulations (EABSS) framework structure
-	Actors (people/groups/organisation)
-	Archetype (role/what they are allowed or expected to do)
-	Social/Psychological aspect (rules or norms)
-	key activities (behaviours performed under certain conditions)
-	Physical component (tools or systems used)
-	Interactions (who talks to or affects whom)
-	Artificial lab (global variables)

Perform thematic analysis on it. Focus only participant responses.
follow these step
1. read the transcript
2. identify components and supporting qoutes under EABSS key components

Please reponse in this format
key component 1
- "code 1"
    - "supporting qoute 1"
    - "supporting qoute 2"
- "code 2"
    - "supporting qoute 1"
    - "supporting qoute 2"
"""
    response = llm.generateContent(prompt)
    return response.text


def pick_codes_qoutes(codes_qoutes: str) -> str:
    prompt = f"""
Based on following codes and qoute of EABSS key components

{codes_qoutes}

Select minimum items from each each components that are the most important to build Agent-based modeling simulation

Please reponse in this format
key component 1
- "code 1"
    - "supporting qoute 1"
    - "supporting qoute 2"
- "code 2"
    - "supporting qoute 1"
    - "supporting qoute 2"
"""
    response = llm.generateContent(prompt)
    return response.text


if __name__ == "__main__":
    print("test")
#     # interview = ""
#     # with open("data/mvp_1.txt", "r") as f:
#     #     interview = f.read()

#     # codesAndQoutes = extract_code_and_qoute(interview)
#     # print(codesAndQoutes)

#     codesAndQoutes = """
#         Okay, here's a thematic analysis of the participant's responses based on the provided EABSS framework:

#     **Actors (people/groups/organisation)**

#     *   **Individual Commuter**
#         *   "I usually wake up around 6:30 a.m., have a light breakfast, and then head out by 7:30."
#         *   "I live about 10 kilometers from my workplace, so I cycle most days."
#     *   **Colleagues**
#         *   "I also sometimes carpool with a colleague if we have early meetings."
#         *   "A few of my colleagues have switched to biking too."
#     *   **General Public/Other Commuters**
#         *   "I talk to friends who say they’d love to bike or take public transport..."
#         *   "...when people choose to cycle, walk, or take public transport, it reduces emissions and traffic congestion."
#     *   **City Planners/Infrastructure Providers**
#         *   "If cities invested more in those systems, I think we’d see a huge change."

#     **Archetype (role/what they are allowed or expected to do)**

#     *   **Environmentally Conscious Commuter**
#         *   "I started thinking more about my carbon footprint..."
#         *   "If I can do something small but consistent, maybe it helps in the long run."
#     *   **Employee Benefitting from Workplace Sustainability Initiatives**
#         *   "They actually have a cycle-to-work scheme, which I joined."
#         *   "We also have secure bike storage and showers, which makes it easier."
#     *   **Advocate for Sustainable Commuting**
#         *   "Sustainable choices should be the convenient ones—not the hard ones."
#         *   "Hopefully, more people will give it a try."

#     **Social/Psychological Aspect (rules or norms)**

#     *   **Environmental Awareness & Guilt**
#         *   "One big factor was learning more about the environmental impact of daily commuting."
#         *   "I was reading articles and listening to podcasts about climate change, and it struck me that transportation is such a big contributor."
#     *   **Intrinsic Motivation & Enjoyment**
#         *   "...it just felt better to be more active in the mornings."
#         *   "Plus, I enjoy it! It’s energizing and gives me time to think."
#     *   **Positive Reinforcement (Health & Financial Benefits)**
#         *   "I feel fitter, and I’m less stressed during rush hour."
#         *   "I also save money on fuel and parking, which adds up."
#     *   **Influence of Workplace Culture**
#         *   "There’s a really nice culture of encouraging sustainable habits there."
#     *   **Frustration with Barriers to Sustainability**
#         *   "...the lack of safe bike lanes or inconsistent bus schedules puts them off."

#     **Key Activities (behaviours performed under certain conditions)**

#     *   **Cycling to Work (Primary)**
#         *   "I cycle most days. It takes me around 35 to 40 minutes, depending on traffic and weather."
#     *   **Taking the Bus (Alternative)**
#         *   "Yes, if it’s raining heavily or I’m feeling unwell, I take the bus."
#     *   **Carpooling (Alternative)**
#         *   "I also sometimes carpool with a colleague if we have early meetings."
#     *   **Reading/Listening to Audiobooks (During Commute)**
#         *   "And when I take the bus, I use the time to read or listen to audiobooks."
#     *   **Advocating for Change**
#         *   "I talk to friends who say they’d love to bike or take public transport..."
#         *   "Definitely more protected bike lanes, and maybe incentives for people to use e-bikes or carpool."

#     **Physical Component (tools or systems used)**

#     *   **Bicycle**
#         *   "So cycling is your main mode of transport?"
#     *   **Bus**
#         *   "Yes, if it’s raining heavily or I’m feeling unwell, I take the bus."
#     *   **Bus Stop**
#         *   "It’s pretty reliable, and there’s a bus stop just a few minutes from my flat."
#     *   **Bike Lanes**
#         *   "Instead of sitting in a jam, I’m cruising past traffic on a bike lane."
#     *   **Cycle-to-Work Scheme**
#         *   "They actually have a cycle-to-work scheme, which I joined."
#     *   **Secure Bike Storage & Showers**
#         *   "We also have secure bike storage and showers, which makes it easier."
#     *   **Roads**
#         *    "depending on traffic and weather"

#     **Interactions (who talks to or affects whom)**

#     *   **Individual influences themselves**
#         * " I started thinking more about my carbon footprint"
#     *   **Individual influences colleagues**
#         *   "A few of my colleagues have switched to biking too."
#     *   **Individual influences friends**
#         *   "I talk to friends who say they’d love to bike or take public transport..."
#     *   **Workplace influences individual**
#         *   "They actually have a cycle-to-work scheme, which I joined."

#     **Artificial Lab (global variables)**

#     *   **Environmental Impact of Transportation**
#         *   "I was reading articles and listening to podcasts about climate change, and it struck me that transportation is such a big contributor."
#     *   **Urban Infrastructure & Policy**
#         *   "Obviously, we need better infrastructure and policy..."
#         *   "If cities invested more in those systems, I think we’d see a huge change."
#     *   **Climate Change**
#          * "I was reading articles and listening to podcasts about climate change, and it struck me that transportation is such a big contributor."

#     This provides a breakdown of the participant's responses categorized within the EABSS framework, which can be used to inform the development of agent-based social simulations.

#     Okay, here's a thematic analysis of the participant's responses based on the provided EABSS framework:

#     **Actors (people/groups/organisation)**

#     *   **Individual Commuter**
#         *   "I usually wake up around 6:30 a.m., have a light breakfast, and then head out by 7:30."
#         *   "I live about 10 kilometers from my workplace, so I cycle most days."
#     *   **Colleagues**
#         *   "I also sometimes carpool with a colleague if we have early meetings."
#         *   "A few of my colleagues have switched to biking too."
#     *   **General Public/Other Commuters**
#         *   "I talk to friends who say they’d love to bike or take public transport..."
#         *   "...when people choose to cycle, walk, or take public transport, it reduces emissions and traffic congestion."
#     *   **City Planners/Infrastructure Providers**
#         *   "If cities invested more in those systems, I think we’d see a huge change."

#     **Archetype (role/what they are allowed or expected to do)**

#     *   **Environmentally Conscious Commuter**
#         *   "I started thinking more about my carbon footprint..."
#         *   "If I can do something small but consistent, maybe it helps in the long run."
#     *   **Employee Benefitting from Workplace Sustainability Initiatives**
#         *   "They actually have a cycle-to-work scheme, which I joined."
#         *   "We also have secure bike storage and showers, which makes it easier."
#     *   **Advocate for Sustainable Commuting**
#         *   "Sustainable choices should be the convenient ones—not the hard ones."
#         *   "Hopefully, more people will give it a try."

#     **Social/Psychological Aspect (rules or norms)**

#     *   **Environmental Awareness & Guilt**
#         *   "One big factor was learning more about the environmental impact of daily commuting."
#         *   "I was reading articles and listening to podcasts about climate change, and it struck me that transportation is such a big contributor."
#     *   **Intrinsic Motivation & Enjoyment**
#         *   "...it just felt better to be more active in the mornings."
#         *   "Plus, I enjoy it! It’s energizing and gives me time to think."
#     *   **Positive Reinforcement (Health & Financial Benefits)**
#         *   "I feel fitter, and I’m less stressed during rush hour."
#         *   "I also save money on fuel and parking, which adds up."
#     *   **Influence of Workplace Culture**
#         *   "There’s a really nice culture of encouraging sustainable habits there."
#     *   **Frustration with Barriers to Sustainability**
#         *   "...the lack of safe bike lanes or inconsistent bus schedules puts them off."

#     **Key Activities (behaviours performed under certain conditions)**

#     *   **Cycling to Work (Primary)**
#         *   "I cycle most days. It takes me around 35 to 40 minutes, depending on traffic and weather."
#     *   **Taking the Bus (Alternative)**
#         *   "Yes, if it’s raining heavily or I’m feeling unwell, I take the bus."
#     *   **Carpooling (Alternative)**
#         *   "I also sometimes carpool with a colleague if we have early meetings."
#     *   **Reading/Listening to Audiobooks (During Commute)**
#         *   "And when I take the bus, I use the time to read or listen to audiobooks."
#     *   **Advocating for Change**
#         *   "I talk to friends who say they’d love to bike or take public transport..."
#         *   "Definitely more protected bike lanes, and maybe incentives for people to use e-bikes or carpool."

#     **Physical Component (tools or systems used)**

#     *   **Bicycle**
#         *   "So cycling is your main mode of transport?"
#     *   **Bus**
#         *   "Yes, if it’s raining heavily or I’m feeling unwell, I take the bus."
#     *   **Bus Stop**
#         *   "It’s pretty reliable, and there’s a bus stop just a few minutes from my flat."
#     *   **Bike Lanes**
#         *   "Instead of sitting in a jam, I’m cruising past traffic on a bike lane."
#     *   **Cycle-to-Work Scheme**
#         *   "They actually have a cycle-to-work scheme, which I joined."
#     *   **Secure Bike Storage & Showers**
#         *   "We also have secure bike storage and showers, which makes it easier."
#     *   **Roads**
#         *    "depending on traffic and weather"

#     **Interactions (who talks to or affects whom)**

#     *   **Individual influences themselves**
#         * " I started thinking more about my carbon footprint"
#     *   **Individual influences colleagues**
#         *   "A few of my colleagues have switched to biking too."
#     *   **Individual influences friends**
#         *   "I talk to friends who say they’d love to bike or take public transport..."
#     *   **Workplace influences individual**
#         *   "They actually have a cycle-to-work scheme, which I joined."

#     **Artificial Lab (global variables)**

#     *   **Environmental Impact of Transportation**
#         *   "I was reading articles and listening to podcasts about climate change, and it struck me that transportation is such a big contributor."
#     *   **Urban Infrastructure & Policy**
#         *   "Obviously, we need better infrastructure and policy..."
#         *   "If cities invested more in those systems, I think we’d see a huge change."
#     *   **Climate Change**
#          * "I was reading articles and listening to podcasts about climate change, and it struck me that transportation is such a big contributor."

#     This provides a breakdown of the participant's responses categorized within the EABSS framework, which can be used to inform the development of agent-based social simulations.
#     """

#     # keyComponents = pick_codes_qoutes(codesAndQoutes)
#     # print(keyComponents)

#     """
#     Okay, here's a selection of the most important items from each EABSS component to build an Agent-Based Model (ABM) simulation for sustainable commuting, focusing on the essentials for a functioning model:

# *   **Actors:** **Individual Commuter** (Fundamental agent to simulate)

# *   **Archetype:** **Environmentally Conscious Commuter** and **Employee Benefitting from Workplace Sustainability Initiatives** (Captures key motivations and constraints.)

# *   **Social/Psychological Aspect:** **Environmental Awareness & Guilt**, **Intrinsic Motivation & Enjoyment**, **Frustration with Barriers to Sustainability** (Crucial for decision-making in the agents).

# *   **Key Activities:** **Cycling to Work (Primary)**, **Taking the Bus (Alternative)** (Core behaviors to simulate and their alternatives)

# *   **Physical Component:** **Bicycle, Bus, Bike Lanes** (Key infrastructure elements that influence behavior)

# *   **Interactions:** **Individual influences themselves**, **Workplace influences individual** (Captures feedback loops and external influences on behavior)

# *   **Artificial Lab:** **Environmental Impact of Transportation, Urban Infrastructure & Policy** (Key global variables that affect the overall simulation environment)

# **Rationale for Selection:**

# *   **Individual Commuter:**  The individual commuter *is* the agent in this ABM.  Without them, there's nothing to simulate.
# *   **Environmentally Conscious Commuter & Employee Benefitting from Workplace Sustainability Initiatives**: these are the main drivers for why agents decide to take sustainable commuting choices.
# *   **Environmental Awareness & Guilt, Intrinsic Motivation & Enjoyment, Frustration with Barriers to Sustainability**:  These elements represent the internal decision-making processes within the agents. They dictate how an agent responds to external factors.
# *   **Cycling to Work & Taking the Bus:** These are the primary and alternative actions that we want to model and see change based on other factors.
# *   **Bicycle, Bus, Bike Lanes:** These are the crucial physical elements that agents interact with and are necessary for simulating movement and accessibility.
# *   **Individual influences themselves & Workplace influences individual:**  These interactions capture key feedback loops. Individuals may change their behavior based on their own experiences (e.g., feeling fitter after cycling), and workplace policies directly affect choices.
# *   **Environmental Impact of Transportation & Urban Infrastructure & Policy:** These elements define the external factors that influence behavior.

# This selection provides a core set of elements that are essential for building a meaningful and functional ABM of sustainable commuting behavior. You can then add complexity by incorporating more elements as needed.

# Okay, here's a selection of the most important items from each EABSS component to build an Agent-Based Model (ABM) simulation for sustainable commuting, focusing on the essentials for a functioning model:

# *   **Actors:** **Individual Commuter** (Fundamental agent to simulate)

# *   **Archetype:** **Environmentally Conscious Commuter** and **Employee Benefitting from Workplace Sustainability Initiatives** (Captures key motivations and constraints.)

# *   **Social/Psychological Aspect:** **Environmental Awareness & Guilt**, **Intrinsic Motivation & Enjoyment**, **Frustration with Barriers to Sustainability** (Crucial for decision-making in the agents).

# *   **Key Activities:** **Cycling to Work (Primary)**, **Taking the Bus (Alternative)** (Core behaviors to simulate and their alternatives)

# *   **Physical Component:** **Bicycle, Bus, Bike Lanes** (Key infrastructure elements that influence behavior)

# *   **Interactions:** **Individual influences themselves**, **Workplace influences individual** (Captures feedback loops and external influences on behavior)

# *   **Artificial Lab:** **Environmental Impact of Transportation, Urban Infrastructure & Policy** (Key global variables that affect the overall simulation environment)

# **Rationale for Selection:**

# *   **Individual Commuter:**  The individual commuter *is* the agent in this ABM.  Without them, there's nothing to simulate.
# *   **Environmentally Conscious Commuter & Employee Benefitting from Workplace Sustainability Initiatives**: these are the main drivers for why agents decide to take sustainable commuting choices.
# *   **Environmental Awareness & Guilt, Intrinsic Motivation & Enjoyment, Frustration with Barriers to Sustainability**:  These elements represent the internal decision-making processes within the agents. They dictate how an agent responds to external factors.
# *   **Cycling to Work & Taking the Bus:** These are the primary and alternative actions that we want to model and see change based on other factors.
# *   **Bicycle, Bus, Bike Lanes:** These are the crucial physical elements that agents interact with and are necessary for simulating movement and accessibility.
# *   **Individual influences themselves & Workplace influences individual:**  These interactions capture key feedback loops. Individuals may change their behavior based on their own experiences (e.g., feeling fitter after cycling), and workplace policies directly affect choices.
# *   **Environmental Impact of Transportation & Urban Infrastructure & Policy:** These elements define the external factors that influence behavior.

# This selection provides a core set of elements that are essential for building a meaningful and functional ABM of sustainable commuting behavior. You can then add complexity by incorporating more elements as needed.
# """
