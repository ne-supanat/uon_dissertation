def generate():
    pass
    # # action decision table
    # df = pd.read_csv("mvp/results/answer_record.csv", sep=";", header=None)
    # df.columns = ["file", "type"] + [f"q{i+1}" for i in range(len(questions))]

    # with open(f"mvp/results/answer_prob.csv", "a+") as f:
    #     for type in Archetype:
    #         archetypeDF = df[df["type"] == type.value]
    #         archetypeSize = archetypeDF.shape[0]

    #         for i in range(len(questions)):
    #             for mode in TransportationMode:
    #                 answerDF = archetypeDF[archetypeDF[f"q{i+1}"] == mode.value]

    #                 prob = answerDF.shape[0] / archetypeSize
    #                 print(f"{type.value};{questions[i]};{mode.value};{prob}")

    #                 f.write(f"{type.value};{questions[i]};{mode.value};{prob}\n")
