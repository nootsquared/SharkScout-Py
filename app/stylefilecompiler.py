import os

class FileComplier:
    def combineFiles():
        kvstyles_directory = 'app/kvstyles/'
        template_filename = 'template.kv'
        combined_kivy_file_path = 'app/mainstyling.kv'
        file_contents = []

        template_file_path = os.path.join(kvstyles_directory, template_filename)
        with open(template_file_path, 'r') as template_file:
            file_contents.append(template_file.read())

        for filename in os.listdir(kvstyles_directory):
            if filename.endswith(".kv") and filename != template_filename:
                file_path = os.path.join(kvstyles_directory, filename)
                with open(file_path, 'r') as file:
                    file_contents.append(file.read())

        combined_kivy_content = '\n'.join(file_contents)

        with open(combined_kivy_file_path, 'w') as combined_file:
            combined_file.write(combined_kivy_content)
