from matplotlib import pyplot as plt

class stats:
    def __init__(self):
        pass
    
    def draw(self, data):
        functionName=list(data.keys())
        
        generatedDataList=[data['Manhattan Distance']['generationCount'],
                           data['Euclidean Distance']['generationCount'],
                           data['Cosine Distance']['generationCount']]
        
        expandCountList=[data['Manhattan Distance']['expandCount'],
                         data['Euclidean Distance']['expandCount'],
                         data['Cosine Distance']['expandCount']]
        
        timeList=[int(data['Manhattan Distance']['time']*1000),
                  int(data['Euclidean Distance']['time']*1000),
                  int(data['Cosine Distance']['time']*1000)]
        
        plt.figure(figsize=(8,6.5))
        plt.subplots_adjust(left=0.18, wspace=0.25, hspace=0.5,
                    bottom=0.05, top=0.95)
        
        plt.subplot(311)
        plt.title('Generated Nodes')
        plt.bar(functionName, generatedDataList)
        # plt.savefig('img/generatedData.png')
        
        plt.subplot(312)
        plt.title('Expanded Nodes')
        plt.bar(functionName, expandCountList)
        # plt.savefig('img/expandCount.png')

        plt.subplot(313)
        plt.title('Time Used (ms)')
        plt.bar(functionName, timeList)
        
        plt.savefig('img/stats.png')

        
        # plt.legend(["Generated", "Expanded","Time"])
        # plt.show()