import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import tensorflow as tf
from keras.utils import to_categorical
import os
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

###=======================================================###

###=======================================================###

def Split_Train_Dev_Test(Num_batches , seed):

    np.random.seed(seed)

    p = np.random.permutation( Num_batches )
    p = p + 1
    p = p.tolist()
    
    # 80 10 10 split
    num_dev =  Num_batches//10
    num_test = Num_batches//10
    
    batch_train = p[0:-(num_dev+num_test)]
    batch_dev = p[-(num_dev+num_test):-num_test]
    batch_test = p[-num_test:]


    return batch_train, batch_dev, batch_test

###=======================================================###

###=======================================================###

def ImportValues(folder,batch):
   # This function loads the x and y values, reshapes X to volume and tranform Y to 1-hot 

    name_img = folder + 'X_Img_Values' + str(batch) + '.npy'
    name_sex = folder + 'X_Sex_Values' + str(batch) + '.npy'
    name_age = folder + 'X_Age_Values' + str(batch) + '.npy'
    namey = folder + 'YValues' + str(batch) + '.npy'
    
    X_img=np.load(name_img)
    X_sex=np.load(name_sex)
    X_age=np.load(name_age)
    Y=np.load(namey)
    Y=np.squeeze(Y)

    # length check
    assert(len(X_img) == len(Y))


    n_classes = 3 # 3 labels: 0:normal, 1:MCI, 2:Alzh

    X_img = np.reshape(X_img,(-1,116,130,83,1)) ######################

#     # choosing a 16 by 16 by 16 slot in the images
    # X_img = X_img[:, 100:108, 100:108, 100:108, :]

    
    
    # change lables to 1-hot form matrix
    Y = to_categorical(Y, n_classes)

    return X_img, X_age, X_sex ,Y


###=======================================================###

###=======================================================###

def my_Scores(y_pred, y_true):
    
    macro    = np.empty([3])
    micro    = np.empty([3])
    weighted = np.empty([3])

    macro[0] = precision_score(y_true, y_pred, average='macro')
    macro[1] = recall_score(y_true, y_pred, average='macro')
    macro[2] = f1_score(y_true, y_pred, average='macro')  

    micro[0] = precision_score(y_true, y_pred, average='micro')  
    micro[1] = recall_score(y_true, y_pred, average='micro') 
    micro[2] = f1_score(y_true, y_pred, average='micro')  

    weighted[0] = precision_score(y_true, y_pred, average='weighted')
    weighted[1] = recall_score(y_true, y_pred, average='weighted') 
    weighted[2] = f1_score(y_true, y_pred, average='weighted') 

    return (macro, micro, weighted)

###=======================================================###

###=======================================================###

def train_neural_network(folder, batch_train, batch_dev, experiment_name , save_name, learning_rate, keep_rate1, keep_rate2, epochs):
  
    epoch_list = list() 
    train_accu_list = list() 
    train_loss_list = list() 
    test_accu_list  = list() 
    mac_score_list  = list() 
    mic_score_list  = list() 
    weigh_score_list = list() 
    tf.reset_default_graph()
    
    #dimensions of our input and output
    n_x = 189
    n_y = 212
    n_z = 135
    n_classes = 3
    
    report_Path = './Report_'+ experiment_name + '/'            # XY_Values: folder for saving X matrix and Y matrix
    if not os.path.exists(report_Path):
        os.makedirs(report_Path)
    # name of the .txt file that is created
    reportFileName = 'Run_Report'

    f = open(report_Path + reportFileName + '.txt', 'w')
    f.write('\n'+'Epoch'+ '\t'+  'Train Set Accuracy'+ '\t'+ 'Test Set Accuracy'+ '\t'+ 'Elapsed time'
            '\t'+ 'mac' + '\t' + 'mic' + '\t' + 'weigh')
    f.close()  
    
 
 
    dev_acc_max = 0
    
#     saver = tf.train.Saver()
    
    with tf.Session() as sess:
        
        new_saver = tf.train.import_meta_graph(save_name + '.meta')
        new_saver.restore(sess, save_name)
        
        
        #load all placeholders and operations

        x_img_input = sess.graph.get_tensor_by_name('Input_img:0' )  
        x_age_input = sess.graph.get_tensor_by_name('Input_age:0' )
        x_sex_input = sess.graph.get_tensor_by_name('Input_sex:0' )
        y_input = sess.graph.get_tensor_by_name('Output:0') 
        cost = sess.graph.get_tensor_by_name('Cost:0' )
        optimizer = sess.graph.get_operation_by_name('Optimizer' )
        prediction = sess.graph.get_tensor_by_name('Prediction/BiasAdd:0')
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y_input, 1))
        accuracy = sess.graph.get_tensor_by_name('accuracy:0')   
        

        #start training as previous model


        saver = tf.train.Saver()
        saver2 = tf.train.Saver()
        
        import datetime

        start_time = datetime.datetime.now()

        num_of_trn_batches = len(batch_train)
        num_of_dev_batches = len(batch_dev)
        # run epochs
        for epoch in range(epochs):
            start_time_epoch = datetime.datetime.now()
            print('Epoch', epoch + 1, 'started', end='')
            epoch_train_loss = 0
            epoch_train_acc = 0
            # mini batch
            Y_pred = np.zeros((0,0))
            Y_true = np.zeros((0,0))
            for itr in range(num_of_trn_batches):
                start_time_batch = datetime.datetime.now()
                mini_batch_x_img , mini_batch_x_age , mini_batch_x_sex , mini_batch_y = ImportValues(folder,batch_train[itr])
                _ , _cost = sess.run([optimizer, cost], 
                                     feed_dict={ x_img_input: mini_batch_x_img, x_age_input: mini_batch_x_age, 
                                                x_sex_input: mini_batch_x_sex, y_input: mini_batch_y})
                
                epoch_train_loss += _cost
                param1, y_pred , y_true = sess.run([accuracy, tf.argmax(prediction, 1), tf.argmax(y_input, 1)], 
                                      feed_dict={ x_img_input: mini_batch_x_img, x_age_input: mini_batch_x_age, 
                                                 x_sex_input: mini_batch_x_sex, y_input: mini_batch_y})
                
                epoch_train_acc += param1
                Y_pred = np.append(Y_pred,y_pred)
                Y_true = np.append(Y_true,y_true)
                end_time_batch = datetime.datetime.now()
                elapsed_time_batch   = end_time_batch - start_time_batch
                print('\n', 'No. of training batches processed: ', itr + 1, ', Elapsed time: ', elapsed_time_batch)

                f = open(report_Path + reportFileName + '.txt', 'a')
                f.write('\n' + 'No. of training batches processed: ' + str(itr + 1) + ', Elapsed time: ' + str(elapsed_time_batch))
                f.close()
            
            mac, mic, weigh = my_Scores(Y_pred, Y_true)
            
            saver.save(sess, './checkpoints_' + experiment_name + '/CNN_trained', global_step = epoch)
            
            epoch_dev_acc = 0
            
            for itr in range(num_of_dev_batches):
                
                mini_batch_x_img , mini_batch_x_age , mini_batch_x_sex , mini_batch_y = ImportValues(folder, batch_dev[itr])
                param2 = sess.run(accuracy, feed_dict={ x_img_input: mini_batch_x_img,
                                    x_age_input: mini_batch_x_age, x_sex_input: mini_batch_x_sex, y_input: mini_batch_y})
                epoch_dev_acc += param2
                
            end_time_epoch = datetime.datetime.now()
            
            train_acc      = epoch_train_acc/num_of_trn_batches
            dev_acc        = epoch_dev_acc/num_of_dev_batches
            train_loss     = epoch_train_loss/num_of_trn_batches
            elapsed_time   = end_time_epoch - start_time_epoch
            
            if dev_acc > dev_acc_max:
                dev_acc_max =  dev_acc
                saver2.save(sess, report_Path + 'CNN_trained_updated')
            
            print('\n', 'Epoch: ', epoch + 1, ', Train Set Accuracy: ' + str(train_acc) +', Test Set Accuracy: ' + 
                  str(dev_acc) + ', Elapsed time: ' + str(elapsed_time))
            f = open(report_Path + reportFileName + '.txt', 'a')
            f.write('\n'+ str(epoch + 1) + '\t' + str(train_acc) + '\t' + str(dev_acc) + '\t' + str(elapsed_time) + '\t' +
                    str(mac) + '\t' + str(mic) + '\t' + str(weigh))
            f.close()
            epoch_list.append(epoch + 1)
            train_accu_list.append(train_acc)
            test_accu_list.append(dev_acc)
            train_loss_list.append(train_loss)
            fig1 = plt.figure(1)
            plt.gcf().clear()
            ax1  = plt.gca()
            ax1.set_xlim([0, epochs + 5])
            ax1.set_ylim([0, 1.1])
            plt.ylabel('Accuracy')
            plt.xlabel('Number of Epochs')
            plt.grid(True)

            plt.plot(epoch_list, train_accu_list, '-b', label = "Training")
            plt.plot(epoch_list, test_accu_list , '-r', label = "Testing" )
            plt.legend(loc='upper left')

            fig2 = plt.figure(2)
            plt.gcf().clear()
            ax2 = plt.gca()
            ax2.set_xlim([0,epochs + 5])
            plt.ylabel('Loss')
            plt.xlabel('Number of Epochs')
            plt.grid(True)

            plt.plot(epoch_list, train_loss_list, '-b', label = "Training")
            plt.legend(loc='upper right')

            fig1.savefig(report_Path + 'Accuracy_VS_Epoch.png',  dpi = fig1.dpi)
            fig2.savefig(report_Path + 'TrainLoss_VS_Epoch.png', dpi = fig2.dpi)
        
            
        end_time = datetime.datetime.now()
        print('Time elapse: ', str(end_time - start_time))


###=======================================================###

###=======================================================###



folder='./XY_Values_BatchSize8_Scaled_total/'
experiment_name = 'Remote_DesktopBatch8_NormalArch_NonAugm_0.4Drop_Continue'

save_name = './checkpoints_Remote_DesktopBatch8_NormalArch_NonAugm_0.4Drop/CNN_trained-0'

Num_batches = 51
seed = 0
    
batch_train, batch_dev, batch_test = Split_Train_Dev_Test(Num_batches , seed)



train_neural_network(folder, batch_train , batch_dev, experiment_name, save_name , learning_rate = 0.0001, keep_rate1 = 0.85, keep_rate2 = 0.85, epochs = 50000)










