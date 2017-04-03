"""
Module for training and visualizing the model
while being trained
"""
import datagen
import model
import os
import tensorflow as tf

# model checkpoint directory
LOGDIR = './save'
# model to be loaded (if any)
MODEL = LOGDIR+'/model-5-3008.ckpt'

# Start an interactive tf session
sess = tf.InteractiveSession()

# Add loss and optimizer to session's graph
loss = tf.reduce_mean(tf.square(tf.subtract(model.y_, model.y)))
train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)

# Initialize all global variables
sess.run(tf.global_variables_initializer())

# Summary for tensorboard
tf.summary.scalar("loss", loss)
merged_summary_op = tf.summary.merge_all()

saver = tf.train.Saver()

# If a model exists, load the model to continue traning
if os.path.exists(MODEL+'.index'):
    print("Loading {}...".format(MODEL))
    saver.restore(sess, MODEL)

# Logs for tensorboard
logs_path = './logs'
summary_writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())

# Hyperparameters
epochs = 10
batch_size = 32

for epoch in range(epochs):
  for i in range(int(datagen.num_images/batch_size)):
    xs, ys = datagen.LoadTrainBatch(batch_size)
    # Run a training step
    train_step.run(feed_dict={model.x: xs, model.y_: ys, model.keep_prob: 0.5})
    if i % 10 == 0:
      xs, ys = datagen.LoadValBatch(batch_size)
      # Evaluate validation loss
      loss_value = loss.eval(feed_dict={model.x:xs, model.y_: ys, model.keep_prob: 1.0})
      print("Epoch: %d, Step: %d, Val-Loss: %g" % (epoch, epoch * batch_size + i, loss_value))

    # Add logs for tensorboard
    summary = merged_summary_op.eval(feed_dict={model.x:xs, model.y_: ys, model.keep_prob: 1.0})
    summary_writer.add_summary(summary, epoch*batch_size+i)

    if i % batch_size == 0:
      # Create model checkpoint
      if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)
      checkpoint_path = os.path.join(LOGDIR, "{}/model-{}-{}.ckpt".format(epoch,epoch,i))
      filename = saver.save(sess, checkpoint_path)
      print("Model saved in file: %s" % filename)

print("Run the command line:\n" \
          "--> tensorboard --logdir=./logs " \
          "\nThen open http://0.0.0.0:6006/ into your web browser")
