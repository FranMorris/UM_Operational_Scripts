#!/bin/bash

#SBATCH --job-name=ostia
#SBATCH --time=2:0:0
#SBATCH --ntasks=1

#SBATCH --account=n02-MRW011379
#SBATCH --partition=serial
#SBATCH --qos=serial

start_date=2021-10-01T00:00:00
end_date=2022-01-01T00:00:00
outpath=/work/n02/n02/franmorr/data_files/ostia/global

cd $outpath

source /work/n02/n02/franmorr/venvs/copermarine/bin/activate
echo "downloading..."
#copernicusmarine subset --dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 --variable analysed_sst --start-datetime ${start_date} --end-datetime ${end_date}
#copernicusmarine subset --dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 --variable sea_ice_fraction --start-datetime ${start_date} --end-datetime ${end_date}
deactivate

start_date_short=2021-10-01
end_date_short=2022-01-01

sst_file=${outpath}/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2_analysed_sst_179.98W-179.98E_89.97S-89.97N_${start_date_short}-${end_date_short}.nc
si_file=${outpath}/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2_sea_ice_fraction_179.98W-179.98E_89.97S-89.97N_${start_date_short}-${end_date_short}.nc
echo "splitting" $sst_file, $si_file

module load cray-hdf5
module load netcdf4
module load cdo

d=$start_date_short
while [ "$d" != "$end_date_short" ]; do
    echo $d
#    $nextd=$(date -I -d "$d + 1 day")
    cdo seldate,$d $sst_file ${d//-}_sst.nc
    cdo seldate,$d $si_file ${d//-}_seaice.nc
    echo "cdo done"
    # next day
    d=$(date -I -d "$d + 1 day")
done

echo "finished"

