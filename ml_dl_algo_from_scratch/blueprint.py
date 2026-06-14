from abc import ABC, abstractmethod



class BluePrint(ABC):

    @abstractmethod
    def make_data(self):
        pass

    @abstractmethod
    def train_test_split(self):
        pass

    @abstractmethod
    def summary_train_test_data(self):
        pass

    @abstractmethod
    def training(self): 
        # add aggregation for Training: for ml Training will contains of fitting on train data
        # for dl, fwd prop, weight update, backward prop will be there
        pass

    @abstractmethod
    def cal_loss_training(self):
        pass

    @abstractmethod
    def cal_loss_testing(self):
        pass




