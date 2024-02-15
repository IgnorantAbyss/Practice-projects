def readata (file_path):
    data = {}
    entities = []
    labels = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.read().strip().split('\n')
        for line in lines:
            entity = line.split("=")[0]
            label = line.split("=")[1]

            entities.append(entity)
            labels.append(label)

        data["entity"] = entities
        data["label"] = labels

        return data
    
if __name__ == "__main__":
    data = readata("ner_training_data2.txt")
    print(data["entity"][:10])
    print(data["label"][:10])

