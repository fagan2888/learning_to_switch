#!/bin/sh

echo "Testing all MyMediaLite algorithms, using MovieLens1M usinc 5fold cross validation"

RATING="rating_prediction"
TEST_DIR=/mnt/hd0/marcotcr/datasets/movielens1M/test
TRAIN_DIR=/mnt/hd0/marcotcr/datasets/movielens1M/train

for  method in MatrixFactorization SigmoidCombinedAsymmetricFactorModel
do
 echo "Running for" $method 
  for i in 1 2 3 4 5
  do
    echo $i
    echo "_________________"
    $RATING --training-file=$TRAIN_DIR/r$i.train --test-file=$TEST_DIR/r$i.test --recommender=$method --file-format=movielens_1m --max-iter-=2 --recommender-options="num_iter=1 num_factors=3" --compute-fit --no-id-mapping
  done
done
