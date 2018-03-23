# Convolutional Neural Network

#### We use tensorFlow to build the Neural Network

import numpy as np 
from keras import regularizers
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

###################################################
###################################################
###################################################

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

###################################################
###################################################
###################################################
### Importing Dataset

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
# X_img = X_img[:, 100:116, 100:116, 100:116, :]

    
    
    # change lables to 1-hot form matrix
    Y = to_categorical(Y, n_classes)

    return X_img, X_age, X_sex ,Y


###################################################
###################################################
###################################################

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

###################################################
###################################################
###################################################

### Definiton of Convolutional Newral Network

def cnn_model(x_img_input ,x_age_input,x_sex_input, n_x , n_y , n_z , prob1, prob2, seed=None ):
    regL = 1.0
    #Definition of the convolution net
    
    # conv => n_x*n_y*n_z
    conv1 = tf.layers.conv3d(inputs=x_img_input, filters=16, kernel_size=[3,3,3], padding='same', activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), name='conv1')
    # conv => n_x*n_y*n_z
    #conv2 = tf.layers.conv3d(inputs=conv1, filters=16, kernel_size=[3,3,3], padding='same', activation=tf.nn.relu, name='conv2')
    # pool => n_x*n_y*n_z/2*2*2
    pool3 = tf.layers.max_pooling3d(inputs=conv1, pool_size=[2, 2, 2], strides=2, name='pool3')

    # conv => n_x*n_y*n_z/2*2*2
    conv4 = tf.layers.conv3d(inputs=pool3, filters=32, kernel_size=[3,3,3], padding='same', activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), name='conv4')
    # conv => n_x*n_y*n_z/2*2*2
    #conv5 = tf.layers.conv3d(inputs=conv4, filters=32, kernel_size=[3,3,3], padding='same', activation=tf.nn.relu, name='conv5')
    # pool => n_x*n_y*n_z/4*4*4
    pool6 = tf.layers.max_pooling3d(inputs=conv4, pool_size=[4, 4, 4], strides=4, name='pool6')

    # conv => n_x*n_y*n_z/4*4*4
    conv7 = tf.layers.conv3d(inputs=pool6, filters=64, kernel_size=[3,3,3], padding='same', activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), name='conv7')
    # conv => n_x*n_y*n_z/4*4*4
    #conv8 = tf.layers.conv3d(inputs=conv7, filters=64, kernel_size=[3,3,3], padding='same', activation=tf.nn.relu, name='conv8')
    # pool => n_x*n_y*n_z/8*8*8
    pool9 = tf.layers.max_pooling3d(inputs=conv7, pool_size=[4, 4, 4], strides=4, name='pool9')

    cnn3d_bn = tf.layers.batch_normalization(inputs=pool9, training=True)

    flattening = tf.reshape(cnn3d_bn, [-1, (n_x//32)*(n_y//32)*(n_z//32)*64 ])
    dense1 = tf.layers.dense(inputs=flattening, units=256, activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), bias_regularizer = regularizers.l2(regL), name='dense1')
    # (1-keep_rate) is the probability that the node will be kept
    dropout1 = tf.layers.dropout(inputs=dense1, rate=1-prob1, training=True)
    
    dense2 = tf.layers.dense(inputs=dropout1, units=64, activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), bias_regularizer = regularizers.l2(regL), name='dropout1') + tf.layers.dense(inputs=x_age_input, units=64, activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), bias_regularizer = regularizers.l2(regL), name='Relu_age') + tf.layers.dense(inputs=x_sex_input, units=64, activation=tf.nn.relu, kernel_regularizer = regularizers.l2(regL), bias_regularizer = regularizers.l2(regL), name='Relu_sex') 
    dropout2 = tf.layers.dropout(inputs=dense2, rate=1-prob2, training=True)

    y_conv = tf.layers.dense(inputs=dropout2, units=3, name='Prediction')
    return y_conv


###################################################
###################################################
###################################################

### Training Neural Network

def train_neural_network(folder, batch_train, batch_dev, experiment_name, learning_rate, keep_rate1, keep_rate2, epochs):
  
    epoch_list = list() 
    train_accu_list = list() 
    train_loss_list = list() 
    test_accu_list  = list() 
    mac_score_list  = list() 
    mic_score_list  = list() 
    weigh_score_list = list() 
    tf.reset_default_graph()
    
    #dimensions of our input and output
    n_x = 116
    n_y = 130
    n_z = 83
    n_classes = 3
    
    report_Path = './Report_'+experiment_name+'/'            # XY_Values: folder for saving X matrix and Y matrix
    if not os.path.exists(report_Path):
        os.makedirs(report_Path)
    # name of the .txt file that is created
    reportFileName = 'Run_Report'

    f = open(report_Path + reportFileName + '.txt', 'w')
    f.write('\n'+'Epoch'+ '\t'+  'Train Set Accuracy'+ '\t'+ 'Test Set Accuracy'+ '\t'+ 'Elapsed time'
            '\t'+ 'mac' + '\t' + 'mic' + '\t' + 'weigh')
    f.close()        
    x_img_input = tf.placeholder(tf.float32, shape=[None, n_x, n_y, n_z, 1], name = 'Input_img' )
    x_age_input = tf.placeholder(tf.float32, shape=[None, 1], name='Input_age' )
    x_sex_input = tf.placeholder(tf.float32, shape=[None, 1], name='Input_sex' )


    prob1 = tf.placeholder_with_default(1.0, shape=(),name='prob1')
    prob2 = tf.placeholder_with_default(1.0, shape=(),name='prob2')

    
    y_input = tf.placeholder(tf.float32, shape=[None, n_classes], name='Output') 

    prediction = cnn_model(x_img_input ,x_age_input,x_sex_input, n_x , n_y , n_z , prob1, prob2, seed = 5  )
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y_input), name='Cost' )

    optimizer = tf.train.AdamOptimizer(learning_rate, name = 'Optimizer').minimize(cost)
    
    correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y_input, 1))
    accuracy = tf.reduce_mean(tf.cast(correct, 'float'), name='accuracy')

  
    dev_acc_max = 0
    
    saver = tf.train.Saver()
    saver2 = tf.train.Saver()

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
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
                                                x_sex_input: mini_batch_x_sex, y_input: mini_batch_y,
                                                prob1: keep_rate1, prob2: keep_rate2})
                
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
                saver2.save(sess, report_Path + 'CNN_trained_best')
            
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
        
            #saver.save(sess, './checkpoints_' + experiment_name + '/CNN_trained',global_step=epoch)

        end_time = datetime.datetime.now()
        print('Time elapse: ', str(end_time - start_time))
        

###################################################
###################################################
###################################################     
        
### Example of Training

folder='./XY_Values_BatchSize8_Scaled_ThreeGroups/'
experiment_name = 'B8_3SimplArch_Aug_0.15AND0.20Drop_3Groups_SxAge_L2Regular1_biasReg1_convReg1'
Num_batches = 204
seed = 0
    
batch_train, batch_dev, batch_test = Split_Train_Dev_Test(Num_batches , seed)

train_neural_network(folder, batch_train , batch_dev, experiment_name , learning_rate = 0.0001, keep_rate1 = 0.15, keep_rate2 = 0.20, epochs = 1000)



