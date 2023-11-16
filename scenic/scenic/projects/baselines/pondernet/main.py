"""Main file for PonderNet."""

from absl import flags
from clu import metric_writers
import jax
import jax.numpy as jnp
import ml_collections
from scenic import app
from scenic.projects.baselines.pondernet import pondernet_trainer
from scenic.projects.baselines.pondernet.pondervit import pondervit
from scenic.train_lib import train_utils

FLAGS = flags.FLAGS


def get_model_cls(model_name: str):
  """Get the model class for the PonderNet project."""
  if model_name == 'pondervit':
    return pondervit.PonderViTMultiLabelClassificationModel
  else:
    raise ValueError(f'Unrecognized model: {model_name}.')


def get_trainer(trainer_name):
  if trainer_name == 'pondernet_trainer':
    return pondernet_trainer.train
  else:
    raise ValueError(f'Unrecognized trainer: {trainer_name}.')


def main(rng: jnp.ndarray, config: ml_collections.ConfigDict, workdir: str,
         writer: metric_writers.MetricWriter):
  """Main function for the PonderNet project."""
  # Build the loss_fn, metrics, and flax_model.
  model_cls = get_model_cls(config.model_name)
  data_rng, rng = jax.random.split(rng)
  dataset = train_utils.get_dataset(
      config, data_rng, dataset_service_address=FLAGS.dataset_service_address)
  trainer = get_trainer(config.trainer_name)
  trainer(
      rng=rng,
      config=config,
      model_cls=model_cls,
      dataset=dataset,
      workdir=workdir,
      writer=writer)


if __name__ == '__main__':
  app.run(main=main)
