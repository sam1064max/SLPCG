def loadBalance(partition, cores):
	length = len(partition)
	if length <= cores: return partition
	partition = sorted(partition, key = len, reverse = True)
	scheduledPartition = partition[:cores]
	for component in partition[cores:]:
		scheduledPartition = sorted(scheduledPartition, key = len)
		scheduledPartition[0] = scheduledPartition[0] + component
	return scheduledPartition