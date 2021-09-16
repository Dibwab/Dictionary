# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 16:41:19 2021

@author: Sanjay
"""

#final

def detail(request):
    user= request.user
    if request.method == 'POST':
        def_val = 0
        usr=UserInfo.objects.get(username=user.username)
        if request.FILES.get('pic'):
            #'''Backed Up Image'''
            def_prof = usr.pic
            #'''New Image stored'''
            usr.pic=request.FILES['pic']
            print(usr.pic.name)
            def_val = usr.ext_check()  
            if def_val>0:
                usr.save()
                #'''Failure Checks'''
                #'''size check'''
                filesize= usr.pic.size
                if filesize > 1048576:
                    setlastimg(usr,def_prof)
                    messages.info(request,"Picture size should be equal to or less than 1 MB")
                    return redirect('detail')

                #'''dimension check'''
                height=usr.height   
                width=usr.width
                if height>500 or width>500:
                    setlastimg(usr,def_prof)
                    messages.info(request,"Picture dimensions should be 500X500 or less")
                    return redirect('detail')  

                #real person check
                concepts = crscheckreal(usr.pic.name)
                for concept in concepts:
                    if concept.name in crscheck:
                        print(concept.name)
                        setlastimg(usr,def_prof)
                        messages.info(request,"No person present in the picture")
                        return redirect('detail')
                
                check2 = prof_face_valid(usr.pic.name)
                #Multiple Face Check
                if check2 > 1:
                    setlastimg(usr,def_prof)
                    messages.info(request,"Multiple Face Detected in the Image. Please input your passport size photo")
                    return redirect('detail')
                #Single or no Face and NSFW check
                else:
                    #Face Check
                    if check2 < 1:
                        setlastimg(usr,def_prof)
                        messages.info(request,"No face detected")
                        return redirect('detail')
                    else:
                        nsfw=prof_nsfw_valid(usr.pic.name)
                        concept = nsfw.outputs[0].data.concepts[0]
                        check1 = concept.name
                        #NSFW check
                        if check1 == 'nsfw':
                            setlastimg(usr,def_prof)
                            messages.info(request,"NSFW content detected")
                            return redirect('detail')
                        #Validated
                        else: 
                            if def_prof != def_profile_pic: 
                                usr.pic.delete()
                                usr.pic = def_prof
                                usr.pic.delete()
                                usr.pic=request.FILES['pic']
            else:
                messages.info(request,"Invalid File Format")
                return redirect('detail')
               
        if request.POST['desc'] != '':
            usr.desc=request.POST['desc']
        usr.save()
        usr=UserInfo.objects.all().filter(username=user.username)
        return render(request,'index.html',{'usrdata':usr}) 
    else:
        return render(request,'detail.html')


#final 2.0

def detail(request):
    user= request.user
    if request.method == 'POST':
        def_val = 0
        usr=UserInfo.objects.get(username=user.username)
        if request.FILES.get('pic'):
            #'''Backed Up Image'''
            def_prof = usr.pic
            #'''New Image stored'''
            usr.pic=request.FILES['pic']
            print(usr.pic.name)
            def_val = usr.ext_check()  
            if def_val>0:
                usr.save()
                #'''Failure Checks'''
                #'''size check'''
                filesize= usr.pic.size
                if filesize > 1048576:
                    setlastimg(usr,def_prof)
                    messages.info(request,"Picture size should be equal to or less than 1 MB")
                    return redirect('detail')

                #'''dimension check'''
                height=usr.height   
                width=usr.width
                if height>500 or width>500:
                    setlastimg(usr,def_prof)
                    messages.info(request,"Picture dimensions should be 500X500 or less")
                    return redirect('detail')  

                #real person check
                concepts = crscheckreal(usr.pic.name)
                for concept in concepts:
                    if concept.name in crscheck:
                        print(concept.name)
                        setlastimg(usr,def_prof)
                        messages.info(request,"No person detected")
                        return redirect('detail')
                
                check2 = prof_face_valid(usr.pic.name)
                #Multiple Face Check
                if check2 > 1:
                    setlastimg(usr,def_prof)
                    messages.info(request,"Upload a passport size appropriate picture")
                    return redirect('detail')
                #Single or no Face and NSFW check
                else:
                    #Face Check
                    if check2 < 1:
                        setlastimg(usr,def_prof)
                        messages.info(request,"Upload a passport size appropriate picture")
                        return redirect('detail')
                    else:
                        nsfw=prof_nsfw_valid(usr.pic.name)
                        concept = nsfw.outputs[0].data.concepts[0]
                        check1 = concept.name
                        #NSFW check
                        if check1 == 'nsfw':
                            setlastimg(usr,def_prof)
                            messages.info(request,"Upload a passport size appropriate picture")
                            return redirect('detail')
                        #Validated
                        else: 
                            if def_prof != def_profile_pic: 
                                usr.pic.delete()
                                usr.pic = def_prof
                                usr.pic.delete()
                                usr.pic=request.FILES['pic']
            else:
                messages.info(request,"Invalid File Format")
                return redirect('detail')
               
        if request.POST['desc'] != '':
            usr.desc=request.POST['desc']
        usr.save()
        usr=UserInfo.objects.all().filter(username=user.username)
        return render(request,'index.html',{'usrdata':usr}) 
    else:
        return render(request,'detail.html')





#original
def detail(request):
    user= request.user
    if request.method == 'POST':
        usr=UserInfo.objects.get(username=user.username)
        if request.FILES.get('pic'):
            '''Backed Up Image'''
            def_prof = usr.pic

            '''New Image stored'''
            usr.pic=request.FILES['pic']
            usr.save()
            nsfw=prof_nsfw_valid(usr.pic.name)
            concept = nsfw.outputs[0].data.concepts[0]
            check1 = concept.name
            check2 = prof_face_valid(usr.pic.name)
            
            '''Validated'''
            valid = 0
            valid= validation(check1,check2)

            '''Failure'''
            if valid > 0:
                print(valid)
                usr.pic.delete()
                usr.pic = def_prof
                usr.save()
                messages.info(request,msg[valid])
                return redirect('detail')
            else:
                if def_prof != def_profile_pic:
                    print(def_prof)
                    def_prof.delete()
        if request.POST['desc'] != '':
            usr.desc=request.POST['desc']
        usr.save()
        usr=UserInfo.objects.all().filter(username=user.username)
        return render(request,'index.html',{'usrdata':usr}) 
    else:
        return render(request,'detail.html')
    
    
    

else:
                if def_prof != def_profile_pic:
                    print(def_prof)
                    def_prof.delete()
        



















from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

metadata = (('authorization', 'Key c32fcb22903e4ffba1aebe227dd6c0e1'),)

with open("nsfw/nsfw6.jpg", "rb") as f:
    file_bytes = f.read()
    
    
post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        model_id="f76196b43bbd45c99b4f3cd8e8b40a8a",
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ]
    ),
    metadata=metadata
)
if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    print("There was an error with your request!")
    print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
    print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
    print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
    raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

# Since we have one input, one output will exist here.
output = post_model_outputs_response.outputs[0]
has_items = bool(output.data.regions)
print(has_items)




ls = output.data.regions[0]
print(output.data.regions.region_info)
print(type(output.data.regions))

for reg in output.data.regions:
    print(reg.region_info)

print(output.data)
if ls is None:
    print('false')
    
else:
    print("true")

has_items = bool(output.data.regions)
print(has_items)
    
    
if output.data is None:    
    print("no face")
else:
    print("face is visible")
ls = []
ls = output.data.regions[0]
print(ls.value)
for l in ls:
    print(l.value)
    print("hello brother")

print("Predicted concepts:")
for concept in output.data.concepts:
    print("%s %.2f" % (concept.name, concept.value))
    
    
    
    
    
    
    
    
    
#Check for face
    
    
with open("abc.jpg.txt", "rb") as f:
    file_bytes = f.read()
    
try:    
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="f76196b43bbd45c99b4f3cd8e8b40a8a",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print("There was an error with your request!")
        print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
        print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
        print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
except:
    print("nahi chala")

# Since we have one input, one output will exist here.
output = post_model_outputs_response.outputs[0]
print(output)
    print(output.data.concepts)
print(type(output.data.concepts))
ls = []
ls = output.data.regions
print(ls)
print(type(ls))
for l in ls:
    #print(l.data.concepts)
    for x in l.data.concepts:
        print(x.name)
    print(type(l.data.concepts))
    dict=l.data
    print(type(l.data))
for concept in output.data.concepts:
    print("%s %.2f" % (concept.name, concept.value))
    
print(output.data.concepts)
has_items = bool(output.data.regions)
if has_items is False:
    print("false")
print(has_items)    


ls=output.data.regions
print(len(ls))









with open("pface2.png", "rb") as f:
    file_bytes = f.read()
    
    
post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        model_id="aaa03c23b3724a16a56b629203edc62c",
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ]
    ),
    metadata=metadata
)
if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    print("There was an error with your request!")
    print("\tCode: {}".format(post_model_outputs_response.outputs[0].status.code))
    print("\tDescription: {}".format(post_model_outputs_response.outputs[0].status.description))
    print("\tDetails: {}".format(post_model_outputs_response.outputs[0].status.details))
    raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

# Since we have one input, one output will exist here.
output = post_model_outputs_response.outputs[0]

for concept in output.data.concepts:
    print("%s %.2f" % (concept.name, concept.value))





ls = []
ls = output.data.regions
print(type(ls))
for l in ls:
    #print(l.data.concepts)
    for x in l.data.concepts:
        print(x.name)
        
        
        
        


            '''size check'''
            filesize= usr.pic.size
            if filesize > 1048576:
                usr.pic.delete()
                usr.pic = def_prof
                usr.save()
                messages.info(request,"Picture size should be equal to or less than 1 MB")
                return redirect('detail')

            '''dimension check'''
            height=usr.height   
            width=usr.width
            print(height)
            print(width)
            if height>500 or width>500:
                usr.pic.delete()
                usr.pic = def_prof
                usr.save()
                messages.info(request,"Picture dimensions should be 500X500 or less")
                return redirect('detail')        

        
        
        
art
sketch     
graphic 
no person


crscheck = ['art','sketch','graphic','no person']

if 'art' in crscheck:
    print('haan hai')
    
        
    
    
    
    
    
    
    
    
import imghdr   
print(imghdr.what('sk1.jpg'))    
    
    
import PIL.Image as img

photo='sk1.jpg'
pic= photo.name
print(i.format)


VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]
    

ls= [photo.endswith(e) for e in VALID_IMAGE_EXTENSIONS]
print(ls)    
if True in ls:
    print('yes')
else:
    print('No')
    
    
    
    
    
if check2 > 1:
                    messages.info(request,"Multiple Face Detected in the Image. Please input your passport size photo")
                    return redirect('detail')
                #Single or no Face and NSFW check
                else:
                    valid = 0
                    nsfw=prof_nsfw_valid(usr.pic.name)
                    concept = nsfw.outputs[0].data.concepts[0]
                    check1 = concept.name
                    valid= validation(check1,check2)
                    #if Present
                    if valid > 0:
                        print(valid)
                        usr.pic.delete()
                        usr.pic = def_prof
                        usr.save()
                        messages.info(request,msg[valid])
                        return redirect('detail')
                    #if Absent
                    else: 
                        if def_prof != def_profile_pic: 
                            usr.pic.delete()
                            usr.pic = def_prof
                            usr.pic.delete()
                            usr.pic=request.FILES['pic']
    
    
    
    
