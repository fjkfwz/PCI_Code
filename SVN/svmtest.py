from svmutil import *

# Specify training set
prob = svm_problem([1, -1], [[1, 0, 1], [-1, 0, -1]])
# Train the model
m = svm_train(prob, '-t 0 -c 1')
# Make a prediction
predicted_labels, _, _ = svm_predict([-1], [[1, 1, 1]], m)
# Predicted label for input [1,1,1] is predicted_labels[0]
svm_save_model('test.model', m)
print str(predicted_labels[0])
