from generate_data import *
from procedures import *

sample=8

segmentstocompare = []
#=============================Figuring out correct ground truth for various algorithms
groundtruth = [x / 4 for x in generate_data.cmuboundaries[sample]]
groundtruthranges = [(1, (0, 2))]
segcompare = []
segmentations = generate_data.segmentations['86 0' + str(sample)]
for point in generate_data.segmentations['86 0' + str(sample)]:
    groundtruthranges.append((point['middle'] / 4, (point['lower'] / 4, point['upper'] / 4)))
averagetruthranges = findtruthranges()
acatruthranges = []
for j, point in enumerate(generate_data.acaboundaries['truth'][sample - 1][1:-1]):
    acatruthranges.append((point, (point - averagetruthranges[i] / 10, point + averagetruthranges[i] / 10)))
#================ Computing boundaries, adding some extra points at the end and start to make comparison easier ========================
fullbatchboundaries = [1] + FullBatch(generate_data.smoldata(sample), len(segmentations), (groundtruth[-1] / len(segmentations)) * 1.5) + [groundtruth[-1]]
minibatchboundaries = [1] + minibatch(generate_data.smoldata(sample), bestminibatchsizes[i]) + [groundtruth[-1]]
#===========Computing scores =============================

fullbatchscore = boundaryevaluate(fullbatchboundaries, groundtruthranges)
fullbatchscore = [round(x, 1) for x in fullbatchscore]
minibatchscore = boundaryevaluate(minibatchboundaries, groundtruthranges)
minibatchscore = [round(x, 1) for x in minibatchscore]
efficientscore = boundaryevaluate(generate_data.othersegmentationstuff[sample - 1], groundtruthranges[:-1])
efficientscore = [round(x, 1) for x in efficientscore]
acascore = boundaryevaluate(generate_data.acaboundaries['aca'][sample - 1], acatruthranges)
acascore = (float(groundtruth[-1]) / generate_data.acaboundaries['aca'][sample - 1][-1] * acascore[0], acascore[1])
acascore = [round(x, 1) for x in acascore]
hacascore = boundaryevaluate(generate_data.acaboundaries['haca'][sample - 1], acatruthranges)
hacascore = (float(groundtruth[-1]) / generate_data.acaboundaries['haca'][sample - 1][-1] * hacascore[0], hacascore[1])
hacascore = [round(x, 1) for x in hacascore]
#===================Readying for comparison =============================================================
segmentstocompare.append((fullbatchboundaries, 'Batch', str(fullbatchscore)))
segmentstocompare.append((minibatchboundaries, 'Minibatch', str(minibatchscore)))
segmentstocompare.append((generate_data.othersegmentationstuff[sample - 1], 'KKV', str(efficientscore)))
segmentstocompare.append((generate_data.acaboundaries['aca'][sample - 1], 'ACA', str(acascore)))
segmentstocompare.append((generate_data.acaboundaries['haca'][sample - 1], 'HACA', str(hacascore)))
comparetotruth((groundtruthranges, 'Truth', ''), segmentstocompare, 1500)
plt.show()