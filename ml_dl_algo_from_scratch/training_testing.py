class Training:
    # we can call particular class of ml or dl as object e.g. obj = LinearRegression()
    # then pass that obj as input in ml_training function along with training data 
    # fit, fit_predict, predict on that data with that object
    def ml_training(training_data, model_obj):
        model_obj.fit(training_data)

    def dl_training(training_data, model_obj):
        self.forward_propagation()
        self.cal_loss()
        self.backward_propagation() # weight updates will happen here
        
    def forward_propagation(self):
        pass
        
    def cal_loss(self):
        pass
        
    def backward_propagation(self):
        pass
    



class Testing:
    pass