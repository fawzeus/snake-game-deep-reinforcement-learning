import torch
import torch.nn as nn
from torch.nn.modules import loss
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_Qnet(nn.Module):
    def __init__(self,input_size,hiden_size,output_size) -> None:
        super().__init__()
        self.linear_in = nn.Linear(input_size,hiden_size)
        self.linear_out = nn.Linear(hiden_size,output_size)
    
    def forward(self,tensor):
        tensor = F.relu(self.linear_in(tensor))
        tensor = self.linear_out(tensor)
        return tensor

    def save(self, file_name="model.pth"):
        dir_path ="./models"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_name = os.path.join(dir_path,file_name)
        torch.save(self.state_dict(),file_name)


class Q_trainer :
    def __init__(self,model,learning_rate,gamma) -> None:
        self.model =model
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(),lr=learning_rate)
        self.loss_function = nn.MSELoss()
    
    def train_step(self,state,action,reward,next_state,done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)


        if len(action.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
        
        #predict the Q with the current state
        Q = self.model(state)
        target = Q.clone()
        for idx in range(len(done)):
            new_Q = reward[idx]
            if not done[idx] :
                new_Q = reward[idx] + self.gamma*torch.max(next_state[idx])
            target[idx][torch.argmax(action).item()] = new_Q
        self.optimizer.zero_grad()
        loss = self.loss_function(target,Q)
        loss.backward()

        self.optimizer.step()
        


