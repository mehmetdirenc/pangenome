import os

def pangenome_combine_ncbi_datasets(main_dataset_folder, combined_file_path):
    cont = False
    with open(combined_file_path, "w") as full_input:
        haplotype = 0
        for root, dirs, files in os.walk(main_dataset_folder):
            if not dirs:
                haplotype += 1
                refseq_id = os.path.basename(root) ##sample_name
                file = [i for i in files if i.endswith('.fna') and "cds" not in i][0]
                genome_file_path = os.path.join(root, file)
                with open(genome_file_path, "r") as genome:
                    for line in genome:
                        if line.startswith(">"):
                            if "plasmid" in line.lower():
                                cont = True
                                continue
                            else:
                                cont = False
                            contig_name = line.replace(" ", "_")
                            full_input.write("#".join([">" + refseq_id, str(haplotype), contig_name.replace(">", "").replace("#", "")]))
                        else:
                            if not cont:
                                if not line.endswith("\n"):
                                    full_input.write(line + "\n")
                                else:
                                    full_input.write(line)
                print(root,dirs,files)

def pangenome_delete_plasmids_ncbi_datasets(main_dataset_folder, non_plasmid_folder):
    cont = False
    for root, dirs, files in os.walk(main_dataset_folder):
        if not dirs:
            file = [i for i in files if i.endswith('.fna') and "cds" not in i][0]
            genome_in_file_path = os.path.join(root, file)
            genome_out_file_path = os.path.join(non_plasmid_folder, file)
            with open(genome_in_file_path, "r") as genome_in, open(genome_out_file_path, "w") as genome_out:
                for line in genome_in:
                    if line.startswith(">"):
                        if "plasmid" in line.lower():
                            cont = True
                            continue
                        else:
                            cont = False
                        genome_out.write(line)
                    else:
                        if not cont:
                            if not line.endswith("\n"):
                                genome_out.write(line + "\n")
                            else:
                                genome_out.write(line)
            print(root,dirs,files)


if __name__ == '__main__':
    main_dataset_folder = "/mnt/lustre/home/mager/magmu818/datasets/c_perfringens/ncbi_dataset_only_complete"
    non_plasmid_folder = "/mnt/lustre/home/mager/magmu818/datasets/c_perfringens/ncbi_dataset_only_complete_no_plasmids_assemblies"
    pangenome_delete_plasmids_ncbi_datasets(main_dataset_folder, non_plasmid_folder)