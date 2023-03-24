def process_post_exec(kernel, args):
    # Print joined command in a post process file.
    with open(kernel.path['tmp'] + '/process/' + str(kernel.process_id) + '.post-exec', 'a') as f:
        f.write(
            ' '.join(['"' + arg + '"' if ' ' in arg else arg for arg in args])
            + '\n'
        )
