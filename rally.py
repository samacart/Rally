import sys

from pyral import Rally, rallyWorkset

class UserStory(object):
	id = None
	name = None
	department = None
	owner = None
	iteration = None

	def set_story(self, id, name, department, owner, iteration):
		self.id = id
		self.name = name
		self.department = department
		self.owner = owner
		self.iteration = iteration
		
		return self
		

class Iteration(object):
	start_date = None
	end_date = None
	name = None
	velocity = None
	user_stories = []

	def set_Iteration(self, start, end, name, velocity, rally_connection):
		self.start_date = start
		self.end_date = end
		self.name = name
		self.velocity = velocity

		self.populate_User_Stories(name, rally_connection)

		return self

	def populate_User_Stories(self, iteration_name, rally_connection):
	        query_criteria = 'Iteration.Name = "%s"' %iteration_name
	        r = rally_connection.get('UserStory', fetch=True, query=query_criteria)
	        if r.errors:
	           sys.stdout.write("\n".join(response.errors))
	           sys.exit(1)

	        for story in r:
		   us = UserStory()
		   if story.Owner <> None:
			   self.user_stories.append(us.set_story(story.FormattedID, story.Name, story.Department, story.Owner.DisplayName, iteration_name))
		   else:
			   self.user_stories.append(us.set_story(story.FormattedID, story.Name, story.Department, 'None', iteration_name))

	def display_User_Stories(self, iteration_name):
		for us in self.user_stories:
			if us.iteration == iteration_name:
				print "\t\t%s\t%s\t%s\t%s" % (us.id, us.name, us.department, us.owner)


class Avant_Rally(object):
	iterations = []
	rally = None

	def __init__(self, project):
		self.project = project

	def connect(self, username, password):
		self.rally = Rally(server, user, password, project=self.project)
		self.rally.enableLogging('rally.simple-use.log')

	def fetch_Iterations(self):
		self.iterations = []

		response = self.rally.get('Iteration', fetch=True)

		for rls in response:
		    iter = Iteration()
		    rlsStart = rls.StartDate.split('T')[0]  # just need the date part
		    rlsDate  = rls.EndDate.split('T')[0]       # ditto
		    self.iterations.append(iter.set_Iteration(rlsStart, rlsDate, rls.Name, rls.PlannedVelocity, self.rally))

	def display_Iterations(self):
		for i in self.iterations:
		    print "\n\n%s   %s  -->  %s\t" % \
		          (i.name, i.start_date, i.end_date)
		    i.display_User_Stories(i.name)


if __name__ == '__main__':

	options = [opt for opt in sys.argv[1:] if opt.startswith('--')]
	server, user, password, apikey, workspace, project = rallyWorkset(options)

	r = Avant_Rally(project)
        r.connect('samacart@gmail.com', 'smkw4eva')

	r.fetch_Iterations()

	r.display_Iterations()

	




