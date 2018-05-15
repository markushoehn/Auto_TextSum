import fastText
import os
import random

TRAINING_DATA_EMBEDDINGS = "data/full_corpus_preprocessed.txt"
LABELED_DATA = "data/labeled_data_binary_fastText.txt"
LABELED_DATA_TEMP =  "data/labeled_data_fastText_temp.txt"
TRAINING_DATA = "data/training_temp.txt"
VALIDATION_DATA = "data/validation_temp.txt"
SUPERVISED_MODEL_TEMP = "data/supervised_model_temp"

# set this to the desired ratio of isNugget to NoNugget instances. isNugget instances will be duplicated if RATIO_NUGGET_TO_NONUGGET > ???
# this heavily influences the costs of missclassifying each label
# -1 if unchanged. We choose to not modify this ratio, since we find it more appropriate as it is right now. We want rather few and meaningful nuggets than otherwise
RATIO_NUGGET_TO_NONUGGET = -1.0

class dataset_manipulator:

    def print_statistics(self, data:str=LABELED_DATA):
        """
        gathers and prints useful statistics about the labeled dataset
        """
        with open(data, "r") as labeled_data:
            count_isNugget = 0
            count_noNugget = 0
            for line in labeled_data:
                tokens = line.strip().split(" ")
                if tokens[0] == "__label__isNugget":
                    count_isNugget += 1
                elif tokens[0] == "__label__noNugget":
                    count_noNugget += 1
                else:
                    print("found weird line: ")
                    print(" ".join(tokens))

            print("Occurences of sentences labeled as isNugget = %d" % count_isNugget)
            print("Occurences of sentences labeled as noNugget = %d" % count_noNugget)
            print("Ratio isNugget to noNugget = %d : %d = %1.2f" % (count_isNugget, count_noNugget, count_isNugget/count_noNugget))
            print("Ratio noNugget to isNugget  = %d : %d = %1.2f" % (count_noNugget, count_isNugget, count_noNugget/count_isNugget))
            print("Hence, missclassifying a noNugget sentence as a Nugget sentence is %1.2f times as costly than to missclassify a Nugget sentence as a nonNugget sentence"%(count_noNugget/count_isNugget))

    def stretch_nugget_ratio(self, desired_ratio:float=RATIO_NUGGET_TO_NONUGGET):
        """
        creates a new (temporary) dataset with the desired Nugget to noNugget Ratio. The name is defined above (LABELED_DATA)
        the file can be automatically deleted by calling the method cleanup()
        """
        if desired_ratio < 0:
            return
        with open(LABELED_DATA, "r") as labeled_data:
            with open(LABELED_DATA_TEMP, "x") as labeled_data_stretched:
                # first read all Nugget instances into a list, also count the current ratio
                # While doing that, already copy all instances into the new file
                nugget_lines = []
                count_isNugget = 0
                count_noNugget = 0
                for line in labeled_data:
                    labeled_data_stretched.write(line)
                    if "__label__isNugget" in line:
                        nugget_lines.append(line)
                        count_isNugget += 1
                    else:
                        count_noNugget += 1

                # add nuggets to the new dataset until the ratio is fullfilled
                current_ratio = count_isNugget/count_noNugget
                nugget_idx = 0
                while current_ratio < desired_ratio:
                    # write next nugget in the (circular) queue
                    labeled_data_stretched.write(nugget_lines[nugget_idx])

                    # update the index for the next nugget that should be appended
                    nugget_idx += 1
                    if nugget_idx == len(nugget_lines):
                        nugget_idx = 0

                    # update ratio
                    count_isNugget += 1
                    current_ratio = count_isNugget/count_noNugget

                print("New Ratio of Nuggets to noNuggets = %d : %d = %1.2f"% (count_isNugget, count_noNugget, current_ratio))

    def split_dataset(self, labeled_dataset:str=LABELED_DATA, validation_share:float=1/3, validation_data:str=VALIDATION_DATA, training_data:str=TRAINING_DATA):
        """
        creates a training and validation dataset from the given labeled data with the given given split indicated by the percentage that should be validation data
        Default is a 1:2 split of validation to training data (1/3 is validation data)
        """
        # we want an even distribution of nuggets and noNuggets in both datasets -> keep them all in lists
        with open(labeled_dataset, "r") as labeled_data:
            # count how many instances of which type are in the dataset and then split for each type according to the ratio
            nugget_lines = []
            noNugget_lines = []
            count_isNugget = 0
            count_noNugget = 0
            for line in labeled_data:
                if "__label__isNugget" in line:
                    nugget_lines.append(line)
                    count_isNugget += 1
                elif "__label__noNugget" in line:
                    noNugget_lines.append(line)
                    count_noNugget += 1

            # calculate how many instances of which type go into each set
            count_validation_isNugget = int(count_isNugget * validation_share)
            count_validation_noNugget = int(count_noNugget * validation_share)
            #count_training_isNugget = count_isNugget - count_validation_isNugget
            #count_training_noNugget = count_noNugget - count_validation_noNugget

            # shuffle data and randomly pick data for the validation set, put the rest into the training set
            random.shuffle(nugget_lines)
            random.shuffle(noNugget_lines)
            with open(validation_data, "x") as validation_set:
                # choose random instances from each label type, write them to the validation set and remove the instance from the respective list
                for i in range(count_validation_isNugget):
                    idx = random.randrange(0, len(nugget_lines))
                    validation_set.write(nugget_lines[idx])
                    nugget_lines.pop(idx)

                for i in range(count_validation_noNugget):
                    idx = random.randrange(0, len(noNugget_lines))
                    validation_set.write(noNugget_lines[idx])
                    noNugget_lines.pop(idx)

            with open(training_data, "x") as training_set:
                # write the remaining instances to the training set
                for line in nugget_lines:
                    training_set.write(line)
                for line in noNugget_lines:
                    training_set.write(line)


    def cleanup(self):
        """
        deletes temporary files
        """
        if os.path.isfile(LABELED_DATA_TEMP):
            os.remove(LABELED_DATA_TEMP)
        if os.path.isfile(TRAINING_DATA):
            os.remove(TRAINING_DATA)
        if os.path.isfile(VALIDATION_DATA):
            os.remove(VALIDATION_DATA)
        if os.path.isfile(SUPERVISED_MODEL_TEMP):
            os.remove(SUPERVISED_MODEL_TEMP)

            

class fastText_classifier:

    def train_internal_model(self, training_data:str=TRAINING_DATA):
        model = fastText.train_supervised(training_data)

        # this code is only temporarily here, it trains and evaluates a model
        print("Testing on validation data")
        n, precision, recall = model.test(VALIDATION_DATA)
        print("On a Validationset of size %d, the model obtained a Precision of %1.4f"%(n, precision))      # precision is around 89.7% :)
        print("Saving model")
        model.save_model(SUPERVISED_MODEL_TEMP)


ft_classifier = fastText_classifier()
manipulator = dataset_manipulator()
manipulator.split_dataset()

print("Training model")
model = ft_classifier.train_internal_model()

manipulator.cleanup()