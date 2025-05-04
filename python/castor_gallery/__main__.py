import os
import glob

import click
from PIL import Image

from . import __version__

@click.version_option(__version__)
@click.group()
@click.pass_context
def castor(ctx):
    """
    This is the main program which allows the construction of pipelines using cogwheel.
    """
    pass


def construct_picture(image, sizes, outdir):

    srcset = ", ".join([os.path.join(outdir, f"{size[0]}-{image}") for size in sizes])
    
    output_tag = f"""
    <div class="row">
      <div class="md-3">
        <picture>
          <source srcset="{srcset}" />
          <img src="512-{image}" class="img-fluid img-thumbnail"/>
        </picture>
      </div>
    </div>
"""

    return output_tag

@click.option("--outdir", "-o", default=None)
@click.argument("directory", default=".")
@castor.command()
def gallery(directory, outdir):
    click.secho(f"Creating a gallery from files in {directory}")

    files = glob.glob(os.path.join(directory, "*.*"))

    sizes = [(128, 128),
             (256, 256),
             (512, 512),
             (1024, 1024),
             (4096, 4096)]
    
    if not outdir:
        outdir = os.path.join(directory, "castor")
    if not os.path.exists(outdir):
        os.makedirs(outdir)


    webpage = ""
        
    for image in files:
        click.echo(f"Opening {image}")
        for size in sizes:
            with Image.open(image) as im:
                if not os.path.exists(os.path.join(outdir, f"{size[0]}-{os.path.basename(image)}")):
                    im.thumbnail(*size)
                    im.save(os.path.join(outdir, f"{size[0]}-{os.path.basename(image)}"))
                im.save(os.path.join(outdir, f"{os.path.basename(image)}"))

        webpage += construct_picture(f"{os.path.basename(image)}", sizes, outdir)

    with open(os.path.join(outdir, "index.html"), "w") as html:
        output = f"""
        <!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-SgOJa3DmI69IUzQ2PVdRZhwQ+dy64/BUtbMJw1MZ8t5HZApcHrRKUc4W0kG879m7" crossorigin="anonymous">
  </head>
  <body>
        {webpage}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/js/bootstrap.bundle.min.js" integrity="sha384-k6d4wzSIapyDyv1kpU366/PK5hCdSbCRGRCMv+eplOQJWyd1fbcAu9OCUj5zNLiq" crossorigin="anonymous"></script>
  </body>
</html>
"""
        html.write(output)
