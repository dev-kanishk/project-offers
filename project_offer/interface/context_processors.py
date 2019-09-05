from model import Categories

def categories_(request):
	return{
	        all_categories: Categories.object.all(),
	        }