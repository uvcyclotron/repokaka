Crabot is run on a an EC2 instance. It has subscribed to the topics related to a particular repo when it is added as a collaborator to a repo.

Command to run Crabot on EC2 instance continuosly even when the ssh connection is lost.


Download the attached pem file and keep in any folder.

Open your terminal in the same folder as the pem file is present and ssh into AWS EC2 instance using the below command:
ssh -i "ec2_crabot.pem" ubuntu@ec2-52-40-143-15.us-west-2.compute.amazonaws.com

Now you navigate to crabot/bot and run the below command to run the bot.
'nohup python main.py & tail -f nohup.out'

nohup is a command that makes the process run even after the ssh connection is lost and the system goes into sleeping state. To kill this process you will need to see the process id of python and kill.

Commands are:
ps -a 
kill pid

If you want to run the bot only for short time then you can simply run it using 'python main.py'

Whenever you make a change to the code of bot you need not stop and rerun the bot. Changes take effect immediately.

# Prereqs

+ JDK8 for `maven`
+ setup `JAVA_HOME`, `JRE_HOME`, and `PATH` 
+ maven

<b>GumTree</b>
Install java on ubuntu using:
sudo apt-get install default-jre
