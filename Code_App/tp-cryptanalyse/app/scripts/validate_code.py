def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        if len(lines1) != len(lines2):
            return False

        for line1, line2 in zip(lines1, lines2):
            if line1.strip() != line2.strip():
                return False
        return True

if __name__ == '__main__':
    if compare_files('output.txt', '/reference/test-encryption.0.out'):
        print("Le code est correct !")
    else:
        print("Le code contient des erreurs.")