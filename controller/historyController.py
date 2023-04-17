from flask import request, jsonify
from model.historyModel import History


def create_history(request):
    search_value = request.json.get('searchValue')
    print("search_value:", search_value)

    try:
        history = History.objects.first()

        history.search_history.append(search_value)
        history.save()

        print("updated_history:", history)
        return jsonify(history), 200

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400


def show_history(request):  
    try:
        history = History.objects.first()
        
        if history:
            current_history = history.search_history
        else:
            current_history = []
                
        return jsonify({"search_history": current_history}), 200
            
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({"error": error_message}), 400
    

    