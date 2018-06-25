from credentials import *
import boto3
from botocore.exceptions import ClientError


#region='us-west-1'
#eng='*'


class DelEBS:
    def __init__(self):
        self.region=region
        self.EBS = boto3.resource('ec2',
                         aws_access_key_id=aws_account['aws_access_key_id'],
                         aws_secret_access_key=aws_account['aws_secret_access_key'],
                         region_name=self.region)
        return self.EBS

    def delete(self):
        for volume in self.EBS.volumes.all():
            print (volume.id, volume.state)
            volume_name = self.EBS.Volume(volume.id)
            try:
                response = volume_name.delete()
                print(response)
            except ClientError as e:
                print("\n Exception in cleanup EBS",e)
        
class DelEC2(DelEBS):
    
    def __init__(self):
        #self.ec2=super().__init__(self)
        self.ec2=DelEBS.__init__(self)
    
    def deleteEC2(self):
        for instance in self.ec2.instances.all():
            instance_name = self.ec2.Instance(instance.id)
            try:
                response = instance_name.terminate()
                print(response)
            except ClientError as e:
                print("\n cleanupallEC2 exception",e)

        
class DelSnapshots(DelEBS):
    def __init__(self):
        self.snap=DelEBS.__init__(self)
        self.region=region
        self.ec2 = boto3.client('ec2',
                         aws_access_key_id=aws_account['aws_access_key_id'],
                         aws_secret_access_key=aws_account['aws_secret_access_key'],
                         region_name=self.region)
        #return self.ec2

    def deletesnaps(self):
        self.snapshot=self.ec2.describe_snapshots(
     
                 Filters=[
              {
                 'Name': 'description',
                 'Values': ['Cloud Snapshot Manager']
                 
             },
#              {
#                 'Name': 'tag:Name',
#                 'Values': [eng+'*']
#                 
#             }
             ],
    
            OwnerIds=['self']
            )
    
        for i in range(0,len(self.snapshot['Snapshots'])):
            self.snapshot_name = self.snap.Snapshot(self.snapshot['Snapshots'][i]['SnapshotId'])
            try:
                response = self.snapshot_name.delete()
                if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
                    print("\n Snapshot deletion of volume id {} Successful".format(self.snapshot['Snapshots'][i]['VolumeId']))
                else:
                    print("\n Snapshot deletion of volume id {} Failed ".format(self.snapshot['Snapshots'][i]['VolumeId']))
                  
            except ClientError as e:
                print("\n  Exception ",e)

class StopInstances(DelSnapshots):
    def __init__(self):
        self.ec2= DelSnapshots.__init__(self)
        

    def stop(self):
        
        instances = self.ec2.describe_instances(Filters=[
                {'Name': 'instance-state-name',
                 'Values': ['running']
                }])
        try:
                
            for i in range(0,len(instances['Reservations'])):
                response= self.ec2.stop_instances(InstanceIds=[instances['Reservations'][i]['Instances'][0]['InstanceId']],
                                       Force=True)
                if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
                    print("\n EC2 stop  {} Successful".format(instances['Reservations'][i]['Instances'][0]['InstanceId']))
                else:
                    print("\n EC2 stop  {} Failed ".format(instances['Reservations'][i]['Instances'][0]['InstanceId']))
                  
                
        except ClientError as e:
                print("\n  Exception while stooping ec2 ",e)
                
            
class fetAllInstaces(StopInstances):
    
    def __init__(self):
        self.ec2= boto3.client('ec2',
                         aws_access_key_id=aws_account['aws_access_key_id'],
                         aws_secret_access_key=aws_account['aws_secret_access_key'],
                         region_name=region)
        
    def getInstances(self):
        instances = self.ec2.describe_instances()
        
            
if __name__ == "__main__":
    
    
    
#   for eng in puneTeam:
#        print("\n Eng",eng)
#        for region in allregions:
#            n =  DelSnapshots()
#            #print("\n d.var",d.var)
#            n.deletesnaps();
      
    #p=StopInstances()
    #p.stop();
    #e=DelEC2()
    #e.deleteEC2()
    

    try:
        
            
        for i in range(0,len(allregions)):
            print("\n Clenup for {}".format(allregions[i]))
            region = allregions[i]
            n = DelSnapshots()
            n.deletesnaps()
    except ClientError as e:
        print("\n Error",e)
   
    
  


