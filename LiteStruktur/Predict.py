import pickle


with open('data.pkl', 'r') as input:
    X = pickle.load(input)
    input.close()
print(X.data)

print(X.target)
