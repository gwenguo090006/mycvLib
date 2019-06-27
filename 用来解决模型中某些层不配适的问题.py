#coding=utf-8
#用来解决模型中某些层不配适的问题


device = torch.device("cuda" if args.cuda else "cpu")
SN=SpotNet().eval()

testImg = utils_old.load_testImage(args.testImgPath)
testImg = testImg.unsqueeze(0).to(device)
state_dict = torch.load(args.model)
model_state_dict=SN.state_dict()
# print(model_state_dict['N1.running_mean'].size())

#只考虑了conv和bn两种情况
for k in list(model_state_dict.keys()):
    print(k)
    conv2dIndex=str(k).find('conv2d',0,len(str(k)))
    if conv2dIndex != -1:#if there is a 'conv2d'，delete it
        keyNew=str(k)[:conv2dIndex] + str(k)[conv2dIndex+7:]
        keyNew=keyNew.replace('_','-')
        model_state_dict[k]=state_dict[keyNew]#caffe命名的层中有'-'，而pytorch使用的是'_'
    elif str(k).endswith('weight'):#bn的weight
        oneSize=model_state_dict[k].shape[0]
        model_state_dict[k]=torch.ones(oneSize)
    elif str(k).endswith('bias'):
        zerosSize=model_state_dict[k].shape[0]
        model_state_dict[k]=torch.zeros(zerosSize)
    else:
        model_state_dict[k]=state_dict[k]

SN.load_state_dict(state_dict)
SN.to(device)