from generateRandomChrome import get_random_chrome
from create_piece import createPiece
from convert_notes_to_xml import convert_to_xml

def main():
    initial_genome = get_random_chrome(10, 32)
    measures = createPiece(initial_genome)
    convert_to_xml(measures)

main()