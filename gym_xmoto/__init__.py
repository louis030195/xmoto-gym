import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Xmoto-v0',
    entry_point='gym_xmoto.envs:XmotoEnv',
)
