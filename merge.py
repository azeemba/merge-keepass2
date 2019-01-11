"""Takes in a list of keepass2 files to merge and
outputs another keepass2 file with the merged results.
"""
import click
from pykeepass import PyKeePass

@click.command()
@click.argument(
    'srcFiles', nargs=-1, type=click.Path(exists=True))
@click.argument(
    'resultFile', nargs=1, type=click.Path(exists=False))
@click.option(
    '--password', prompt=True, hide_input=True,
    envvar='KEEPASS_PASSWORD',
    help=('The password for keepass. '
    'You will be prompted if not provided. '
    'Use `--password ""` if your database is only protected by '
    'a keyfile. '
    'Environment variable KEEPASS_PASSWORD can be set as well'))
@click.option(
    '--keyfile', prompt=False,
    envvar='KEEPASS_KEYFILE',
    help=('The path of a keyfile for keepass (optional). '
    'Environment variable KEEPASS_KEYFILE can be set as well'))
def main(srcfiles, resultfile, password, keyfile):
    """Merge all keepass SRCFILES into a new file named RESULTFILE.
    Password for all files must be the same.
    """
    sources = [PyKeePass(p, password, keyfile) for p in srcfiles]
    uuids = set()
    dest = None
    for source in sources:
        uuids = uuids.union(set([e.uuid for e in source.entries]))
        if dest is None:
            dest = source
        elif len(dest.entries) < len(source.entries):
            dest = source

    print(uuids)
    for uuid in uuids:
        latest_entry = None
        for source in sources:
            entry = source.find_entries_by_uuid(uuid, first=True)
            if latest_entry is None:
                latest_entry = entry
            elif entry is not None and entry.mtime > latest_entry.mtime:
                latest_entry = entry
        dest_entry = dest.find_entries_by_uuid(uuid, first=True)

        def set_if_exists(a, b, prop):
            val = getattr(a, prop)
            if val:
                setattr(b, prop, val)
        
        if dest_entry:
            set_if_exists(latest_entry, dest_entry, 'title')
            set_if_exists(latest_entry, dest_entry, 'username')
            set_if_exists(latest_entry, dest_entry, 'password')
            set_if_exists(latest_entry, dest_entry, 'url')
            set_if_exists(latest_entry, dest_entry, 'notes')
            set_if_exists(latest_entry, dest_entry, 'expiry_time')
            set_if_exists(latest_entry, dest_entry, 'tags')
            set_if_exists(latest_entry, dest_entry, 'icon')
        else:
            raise Exception("Not tested yet")
            dest.add_entry(
                dest.root_group,
                latest_entry.title,
                latest_entry.username,
                latest_entry.password,
                latest_entry.url,
                latest_entry.notes,
                latest_entry.expiry_time,
                latest_entry.tags,
                latest_entry.icon
            )
            dest.uuid = latest_entry.uuid
    
    dest.save(resultfile)
        

if __name__ == "__main__":
    # pylint: disable-all
    main()