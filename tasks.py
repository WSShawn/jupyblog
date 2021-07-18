from invoke import task


@task
def setup(c, version=None):
    """
    Setup dev environment, requires conda
    """
    version = version or '3.8'
    suffix = '' if version == '3.8' else version.replace('.', '')
    env_name = f'jupyblog{suffix}'

    c.run(f'conda create --name {env_name} python={version} --yes')
    c.run('eval "$(conda shell.bash hook)" '
          f'&& conda activate {env_name} '
          '&& pip install --editable .[dev]')

    print(f'Done! Activate your environment with:\nconda activate {env_name}')


@task
def docs_serve(c):
    with c.cd('docs'):
        c.run('jupyblog')

    c.run('mkdocs serve')
