"""Import AWS resources into terraform."""
import argparse
import sys
from etisalat.terraform.importer import AwsImporter
from etisalat.terraform.converter import Converter
from etisalat.terraform.initialiser import Initialiser
from etisalat.terraform.validator import Validator


class Terraformer():
    """Import AWS resources into terraform."""

    def parse(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description="Import existing AWS resources into Terraform.")
        parser.add_argument("command", help="AWS to Terraform command to run.",
                            choices=["import", "convert", "complete", "init", "validate"])
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, "_{}".format(args.command)):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        getattr(self, "_{}".format(args.command))()

    def _common_args(self, parser):
        parser.add_argument(
            '--resource-type', help='Resource type to use')
        parser.add_argument(
            '--resource-group', help='Resource group to use', required=True)
        parser.add_argument('--region', default='eu-west-1', help='AWS region')
        parser.add_argument('--profile', default='prod',
                            help='AWS credential profile to use')

    def _validate(self):
        parser = argparse.ArgumentParser(
            description="Validate Terraform resource configuration.")
        self._common_args(parser)
        args = parser.parse_args(sys.argv[2:])
        Validator(args).validate()

    def _init(self):
        parser = argparse.ArgumentParser(
            description="Initialise a resource group directory for Terraform.")
        self._common_args(parser)
        args = parser.parse_args(sys.argv[2:])
        Initialiser(args).initialise()

    def _convert(self):
        parser = argparse.ArgumentParser(
            description="Convert terraform state to terraform configuration.")
        self._common_args(parser)
        args = parser.parse_args(sys.argv[2:])
        Converter(args).convert_states()

    def _import(self):
        parser = argparse.ArgumentParser(
            description="Import existing AWS resources into terraform state.")
        self._common_args(parser)
        args = parser.parse_args(sys.argv[2:])
        AwsImporter(args).import_resources()

    def _complete(self):
        parser = argparse.ArgumentParser(
            description="Import AWS resources and convert to "
                        "terraform configuration.")
        self._common_args(parser)
        args = parser.parse_args(sys.argv[2:])
        Initialiser(args).initialise()
        AwsImporter(args).import_resources()
        Converter(args).convert_states()
        Validator(args).validate()


def main():
    """Entry point method."""
    Terraformer().parse()

if __name__ == "__main__":
    main()
