import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import random
import pickle
import os

class Chatbot:
    def __init__(self):
        self.pipeline=None
        self.responses={}
        self.is_trained=False
        
    def prepare_data(self):
        """Prepare training data with intents and patterns"""
        intents_data={
            'greeting': 
            {
                'patterns':
                [
                    'hello', 'hi', 'hey', 'good morning', 'good evening', 
                    'good afternoon', 'howdy', 'greetings', 'what\'s up',
                    'hi there', 'hello there', 'good day'
                ],
                'responses':
                [
                    'Hello! How can I help you today?',
                    'Hi there! What can I do for you?',
                    'Greetings! How may I assist you?',
                    'Hello! Nice to meet you!'
                ]
            },
            'goodbye':
            {
                'patterns':
                [
                    'bye', 'goodbye', 'see you later', 'farewell', 'take care',
                    'see you', 'catch you later', 'until next time', 'adios',
                    'see ya', 'bye bye', 'talk to you later'
                ],
                'responses':
                [
                    'Goodbye! Have a wonderful day!',
                    'See you later! Take care!',
                    'Farewell! It was nice talking to you!',
                    'Bye! Come back anytime!'
                ]
            },
            'thanks':
            {
                'patterns':
                [
                    'thanks', 'thank you', 'thx', 'appreciate it', 'thanks a lot',
                    'thank you so much', 'much appreciated', 'grateful'
                ],
                'responses':
                [
                    'You\'re welcome!',
                    'Happy to help!',
                    'No problem at all!',
                    'Glad I could assist you!'
                ]
            },
            'help':
            {
                'patterns':
                [
                    'help', 'can you help me', 'i need help', 'assist me',
                    'what can you do', 'how can you help', 'support'
                ],
                'responses':
                [
                    'I can help you with basic conversations! Try greeting me, asking questions, or saying goodbye.',
                    'I\'m here to chat with you! You can ask me about my capabilities or just have a conversation.',
                    'I can respond to greetings, farewells, and general questions. What would you like to know?'
                ]
            },
            'name':
            {
                'patterns':
                [
                    'what is your name', 'who are you', 'what are you called',
                    'your name', 'tell me your name', 'what should i call you'
                ],
                'responses':
                [
                    'I\'m a chatbot created with Python and machine learning!',
                    'You can call me ChatBot. I\'m an AI assistant.',
                    'I\'m your friendly AI chatbot, here to help and chat!'
                ]
            },
            'age':
            {
                'patterns':
                [
                    'how old are you', 'what is your age', 'age', 'when were you born',
                    'how long have you existed'
                ],
                'responses':
                [
                    'I don\'t have an age like humans do. I exist as long as I\'m running!',
                    'I\'m timeless! I was created recently but don\'t age like people.',
                    'Age is just a number for AI like me. I\'m as old as my last update!'
                ]
            },
            'weather':
            {
                'patterns':
                [
                    'weather', 'how is the weather', 'is it raining', 'sunny today',
                    'what\'s the weather like', 'temperature'
                ],
                'responses':
                [
                    'I don\'t have access to real-time weather data, but I hope it\'s nice where you are!',
                    'I can\'t check the weather, but you could try a weather app or website!',
                    'Sorry, I don\'t have weather information. Try checking your local weather service!'
                ]
            },
            'unknown':
            {
                'patterns': [],
                'responses':
                [
                    'I\'m not sure I understand. Could you rephrase that?',
                    'That\'s interesting, but I\'m not sure how to respond to that.',
                    'I don\'t quite get that. Can you try asking something else?',
                    'Hmm, I\'m still learning. Could you ask me something different?'
                ]
            }
        }
        
        # Convert to training format
        patterns = []
        labels = []
        
        for intent, data in intents_data.items():
            self.responses[intent] = data['responses']
            for pattern in data['patterns']:
                patterns.append(pattern.lower())
                labels.append(intent)
        
        return patterns, labels
    
    def trainModel(self):
        """Train the chatbot model with hyperparameter tuning"""[1]
        print("Preparing training data...")
        patterns, labels = self.prepare_data()
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            patterns, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print("Training model with hyperparameter optimization...")
        
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])
        
        parameters = {
            'tfidf__max_df': [0.8, 0.9, 1.0],
            'tfidf__min_df': [1, 2],
            'tfidf__ngram_range': [(1, 1), (1, 2)],
            'clf__alpha': [0.1, 0.5, 1.0]
        }
        
        grid_search = GridSearchCV(pipeline, parameters, cv=5, scoring='accuracy', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        self.pipeline = grid_search.best_estimator_
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel trained successfully!")
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Cross-validation score: {grid_search.best_score_:.3f}")
        print(f"Test accuracy: {accuracy:.3f}")
        print(f"Classification Report:")
        print(classification_report(y_test, y_pred))
        
        self.is_trained = True
        
    def predictIntent(self, message):
        """Predict the intent of a user message"""
        if not self.is_trained:
            return 'unknown', 0.0

        probabilities=self.pipeline.predict_proba([message.lower()])[0]
        classes=self.pipeline.classes_
        
        max_prob_idx=probabilities.argmax()
        confidence=probabilities[max_prob_idx]
        predicted_intent=classes[max_prob_idx]
        
        if confidence<0.3:
            return 'unknown', confidence
            
        return predicted_intent, confidence
    
    def getResponse(self, message):
        """Generate a response based on the predicted intent"""
        intent, confidence=self.predictIntent(message)
        
        if intent in self.responses:
            response=random.choice(self.responses[intent])
        else:
            response=random.choice(self.responses['unknown'])
            
        return response, intent, confidence
    
    def saveModel(self, filepath='chatbot_model.pkl'):
        """Save the trained model"""
        if self.is_trained:
            with open(filepath,'wb') as f:
                pickle.dump({
                    'pipeline':self.pipeline,
                    'responses':self.responses,
                    'is_trained':self.is_trained
                }, f)
            print(f"Model saved to {filepath}")
        else:
            print("No trained model to save!")
    
    def loadModel(self, filepath='chatbot_model.pkl'):
        """Load a pre-trained model"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                data=pickle.load(f)
                self.pipeline=data['pipeline']
                self.responses=data['responses']
                self.is_trained=data['is_trained']
            print(f"Model loaded from {filepath}")
            return True
        else:
            print(f"Model file {filepath} not found!")
            return False
    
    def runChat(self):
        """Run the chat interface"""
        print("="*60)
        print("🤖 CHATBOT")
        print("="*60)
        print("Welcome! I'm your AI chatbot assistant.")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'retrain' to retrain the model.")
        print("Type 'save' to save the current model.")
        print("-"*60)
        
        while True:
            try:
                user_input=input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit']:
                    print("🤖 Bot: Goodbye! Thanks for chatting with me! 👋")
                    break
                elif user_input.lower()=='retrain':
                    print("🤖 Bot: Retraining the model...")
                    self.trainModel()
                    print("🤖 Bot: Model retrained successfully!")
                    continue
                elif user_input.lower()=='save':
                    self.saveModel()
                    continue
                
                if self.is_trained:
                    response, intent, confidence = self.getResponse(user_input)
                    print(f"🤖 Bot: {response}")
                else:
                    print("🤖 Bot: I need to be trained first! Type 'retrain' to train me.")
                    
            except KeyboardInterrupt:
                print("\n🤖 Bot: Goodbye! Thanks for chatting! 👋")
                break
            except Exception as e:
                print(f"🤖 Bot: Sorry, I encountered an error: {e}")

def main():
    """Main function to run the chatbot"""
    chatbot=Chatbot()
    
    # Try to load existing model, otherwise train a new one
    if not chatbot.loadModel():
        print("No existing model found. Training a new model...")
        chatbot.trainModel()
        chatbot.saveModel()
    
    chatbot.runChat()

if __name__=="__main__":
    main()