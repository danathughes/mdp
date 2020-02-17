## transition.py
##
## Definition of a transition functions and interface.

import numpy as np

class AbstractTransition:
	"""
	An abstract representation of transitions (i.e., dynamics) of an
	environment.
	"""

	def __init__(self):
		"""
		Create a new transition function.
		"""

		pass


	def __call__(self, state, action, next_state):
		"""
		Return the probability of transitioning to next_state, given state and
		action.
		"""

		raise NotImplementedError

	## TODO: Figure out which other parameters should be set here



class DiscreteTransition(AbstractTransition):
	"""
	DiscreteTransition represents the transition function as a 3D tensor of the
	form (state x action x next_state).
	"""

	def __init__(self, num_states, num_actions, initial_value = 0):
		"""
		Create a discrete transition function for the provided state and action
		space dimensionality.

		num_states    - the number of states in the transition model
		num_actions   - the number of actions in the transition model
		initial_value - (optional) the value to initialize each probability to
		                Default value is 0.
		"""

		AbstractTransition.__init__(self)

		self.num_states = num_states
		self.num_actions = num_actions

		# Represent the transition function internally using a numpy array.  
		# Initialize the array to the provided initial value.
		self.__transition = np.ones((self.num_states, self.num_actions, self.num_states))
		self.__transition *= initial_value


	def set(self, state, action, next_state, probability):
		"""
		Set the probability of the transition provided.  

		Multiple transitions can be set simulataneously by passing iterable
		objects for the state, action, next_state, and probability arguments.
		In the event that 
		"""

		self.__transition[state, action, next_state] = probability


	def __call__(self, state, action, next_state):
		"""
		Return the probability of transitioning to next_state from state when
		action is performed
		"""

		# TODO: Validate that state, action, and next state are within range

		return self.__transition[state,action,next_state]


	def __getitem__(self, index):
		"""
		Returns the probability of transitioning to next_state from state when
		action is performed.  Allows for slicing among multiple dimensions.
		"""

		# TODO: Validate that state, action, and next state are within range

		return self.__transition[index]


	def __setitem__(self, index, value):
		"""
		Sets the transition probabilit(ies) at the index to the provided value
		"""

		self.__transition[index] = value


	def sample(self, state, action, shape = None):
		"""
		Generate a sample of the next_state given the state / action pair.

		state  - current state
		action - action performed
		shape (optional) - the number of samples to produce.  If 'None',
		                   produce a single sample, otherwise, produce a
		                   numpy array of samples in the provided shape.
		"""

		# TODO: Validate that state, action, and next state are within range

		# What's the distribution over the next_state
		state_distribution = self[state, action,:]

		# Pick a state given the distribution.  If a shape is provided, create
		# a set of samples conforming to the shape
		if shape is None:
			return np.random.choice(range(self.num_states), p=state_distribution)
		else:
			return np.random.choice(range(self.num_states), size=shape, p=state_distribution)























class SymbolicTransition(AbstractTransition):
	"""
	SymbolicTransition is a wrapper for a DiscreteTransition so that symbolic
	representations of states and actions can be used in lieu of enumerated 
	values.
	"""

	def __init__(self, base_transition, state_map, action_map):
		"""
		Create a discrete transition function for the provided state and action
		space dimensionality.

		num_states    - the number of states in the transition model
		num_actions   - the number of actions in the transition model
		initial_value - (optional) the value to initialize each probability to
		                Default value is 0.
		"""

		AbstractTransition.__init__(self)

		self.__transition = base_transition
		self.state_map = state_map
		self.action_map = action_map


	def set(self, state, action, next_state, probability):
		"""
		Set the probability of the transition provided.  

		Multiple transitions can be set simulataneously by passing iterable
		objects for the state, action, next_state, and probability arguments.
		In the event that 
		"""

		state_num = self.state_map(state)
		action_num = self.action_map(action)
		next_state_num = self.state_map(next_state)

		self.__transition[state_num, action_num, next_state_num] = probability


	def __call__(self, state, action, next_state):
		"""
		Return the probability of transitioning to next_state from state when
		action is performed
		"""

		# TODO: Validate that state, action, and next state are within range

		state_num = self.state_map(state)
		action_num = self.action_map(action)
		next_state_num = self.state_map(next_state)

		return self.__transition(state_num, action_num, next_state_num)


	def __getitem__(self, index):
		"""
		Returns the probability of transitioning to next_state from state when
		action is performed.  Allows for slicing among multiple dimensions.
		"""

		# TODO: Validate that state, action, and next state are within range
		# TODO: Assert that index is a tuple

		state_num = self.state_map(index[0])
		action_num = self.action_map(index[1])
		next_state_num = self.state_map(index[2])

		return self.__transition(state_num, action_num, next_state_num)


	def __setitem__(self, index, value):
		"""
		Sets the transition probabilit(ies) at the index to the provided value
		"""

		state_num = self.state_map(index[0])
		action_num = self.action_map(index[1])
		next_state_num = self.state_map(index[2])

		self.__transition[state_num, action_num, next_state_num] = value


	def sample(self, state, action):
		"""
		Generate a sample of the next_state given the state / action pair.

		state  - current state
		action - action performed
		"""

		# TODO: Validate that state, action, and next state are within range
		state_num = self.state_map(state)
		action_num = self.action_map(action)

		next_state_num = self.__transition.sample(state_num, action_num)

		return self.state_map[next_state_num]
