import os

files_to_fix = [
    'core/templates/core/base.html',
    'core/templates/core/projects.html',
    'core/templates/core/blog_list.html'
]

for file_path in files_to_fix:
    full_path = os.path.join('d:/deepmind_website/deepminds_django', file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple search and replace for the known problematic tags
        # Fixing the footer tag
        old_footer = '{{ site_settings.footer_text|default:"We build dependable AI systems — research,\n            productization, and production operations." }}'
        new_footer = '{{ site_settings.footer_text|default:"We build dependable AI systems — research, productization, and production operations." }}'
        content = content.replace(old_footer, new_footer)
        
        # Fixing the project date tag
        old_project_date = '{{ project.created_at|date:"F Y"\n              }}'
        new_project_date = '{{ project.created_at|date:"F Y" }}'
        content = content.replace(old_project_date, new_project_date)
        
        # Fixing any other multi-line {{ ... }} tags
        import re
        content = re.sub(r'\{\{([^\}]+)\}\}', lambda m: m.group(0).replace('\n', ' ').replace('  ', ' '), content)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file_path}")
    else:
        print(f"File not found: {file_path}")
