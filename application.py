import os

from grader import application

if __name__ == '__main__':
    context = (os.path.join(application.instance_path, 'dev.cert'), 
        os.path.join(application.instance_path, 'dev_cert.key'))

    # application.run(debug=True, ssl_context=context)
    application.run(debug=True)
