###
# find_replace_mask.py
#   Billy Zoellers, Dean Dorton
#
#   Find a list of CUCM translation patterns that have a calledPartyTransformationMask of <mask_to_find>.
#   If a <mask_to_replace_with> is defined, offer to replace the calledPartyTransformationMask.
#
#   find_replace_mask.py <mask_to_find> <optional: mask_to_replace_with>
###


#########
CUCM_USER = "ccmadministrator"
CUCM_PASS = "password"
CUCM_HOST = "cucm.host"
CUCM_VER = "11.5"
#########

import sys
from ciscoaxl import axl
from zeep.exceptions import Fault
from rich.console import Console
from rich.table import Table

###
# Execution starts here
###
def main(argv):
  # Establish a console and UCM object
  console = Console()
  ucm = axl(
    username=CUCM_USER,
    password=CUCM_PASS,
    cucm=CUCM_HOST,
    cucm_version=CUCM_VER
  )

  # Get matching translation patterns from UCM
  find_mask = argv[1]
  patterns = ucm.get_translations()
  replace_patterns = [pattern for pattern in patterns if pattern['calledPartyTransformationMask'] in find_mask]
  console.print(patterns_table(replace_patterns))

  # Stop execution if a replace_mask was not provided
  if (len(argv) < 3):
    exit()
  replace_with = argv[2]
  
  # Confirm before making change
  print(f"The calledPartyTransformationMask of the patterns shown above will be replaced with '{replace_with}'.")
  if not confirm_continue():
    print("No changes made.")
    exit()

  # Replace the calledPartyTransformationMask for each pattern, get an updated copy of each pattern to confirm
  replaced_patterns = []
  for pattern in replace_patterns:
    update_mask = ucm.update_translation(uuid=pattern['uuid'], calledPartyTransformationMask=replace_with)

    if isinstance(update_mask, Fault):
      raise Exception(update_mask)
    replaced_patterns.append(ucm.get_translation(uuid=update_mask['return'])['return']['transPattern'])

  console.print(f'Updated all calledPartyTransformationMask to {replace_with}')
  console.print(patterns_table(replaced_patterns))

###
# Accept a list of translation patterns
#   Return a table for Rich to print to console
###
def patterns_table(patterns):
  table = Table(show_header=True, header_style="bold red")
  table.add_column("Pattern")
  table.add_column("calledPartyTransformationMask")
  table.add_column("Description")

  for pattern in patterns:
    table.add_row(
      pattern['pattern'],
      pattern['calledPartyTransformationMask'],
      pattern['description']
    )

  return table

###
# Confirm that the users wishes to continue
#   Return True if yes, else return False
###
def confirm_continue():
  confirm = input("Enter YES to continue: ")
  if confirm.upper() == 'YES':
    return True

  return False

###
# Check for appropriate number of sys.argv, call main()
###
if __name__ == '__main__':
  if len(sys.argv) < 2:
    print(" usage: find_replace_mask.py <mask_to_find> <optional: mask_to_replace_with>")
    exit()
  main(sys.argv)
