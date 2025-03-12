Image Classification with CNN using PyTorch
This project implements an image classification model using a Convolutional Neural Network (CNN) with PyTorch. The model is trained on the CIFAR-10 dataset to classify images into one of ten categories.

Project Overview
Dataset: CIFAR-10 (Airplane, Automobile, Bird, Cat, Deer, Dog, Frog, Horse, Ship, Truck).
Model: CNN with 3 convolutional layers and 2 fully connected layers.
Optimizer: Adam Optimizer.
Loss Function: CrossEntropyLoss.
Evaluation: Computes accuracy on test data.
Visualization: Displays 10 sample images with actual and predicted labels.

Model Architecture
The CNN model consists of:

3 Convolutional Layers (32, 64, 128 filters)
Max-Pooling Layers (2x2)
Fully Connected Layers (Flattened input → 128 → 10)
Activation Function: ReLU
Final Output Layer: Softmax (for classification)


Findings & Observations
✅ Model Performance:

The CNN achieved ~70-80% accuracy on the test set.
It performed well on distinct images (e.g., ships, trucks).
It struggled with similar categories (e.g., cats vs. dogs).

✅ Challenges Faced:

Small dataset size caused overfitting.
Misclassifications occurred due to visual similarities in classes.
Increasing epochs slightly improved accuracy but required more training time.

✅ Future Improvements:

Data Augmentation: Apply transformations to improve generalization.
More Layers: Experiment with deeper architectures for better feature extraction.
Hyperparameter Tuning: Optimize learning rate, batch size, and dropout.

Conclusion
This project demonstrates how to build, train, and evaluate an image classification model using CNNs in PyTorch. Although our model performed well, further optimizations and enhancements can improve accuracy.
