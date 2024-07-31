import os

from Invoice import Invoice


def train():
    print("training started...")
    training_files = os.listdir("./document_similarity/train")
    for file in training_files:
        invoice = Invoice(file, 'train')
        invoice.save()
    print("training finished...")


def test():
    print("showing up the test results...")
    test_files = os.listdir("./document_similarity/test")
    for file in test_files:
        invoice = Invoice(file, 'test')
        similar_templates = invoice.get_similar_templates()
        for sim in similar_templates:
            print(f"\n\t the file {file} has matching percentage of {sim['matching_percentage']} with {sim['template']}")

    print("\n")
    print("testing finished...")
