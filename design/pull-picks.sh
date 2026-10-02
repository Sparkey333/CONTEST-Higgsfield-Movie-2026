#!/usr/bin/env bash
# Matter of Light — pull every picked clip in cut order, then build a rough assembly.
# Run on your Mac:  bash pull-picks.sh        (needs curl; ffmpeg only for the assembly — brew install ffmpeg)
# Files are named NN_SHOT_take.mp4 so a folder sort IS the cut. The assembly below applies Change 1 from the
# virality read: the first 5s of S15 play before S13, the rest of S15 stays in place. Everything else is whole —
# no ending is ever shortened. The one thing this cannot do is lay the S1 voice: do that in Resolve (A2, 00:00:01:00).
set -e
mkdir -p picks alternates && cd picks

curl -sSfL -o 01_S1_f84a308f.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_174858_f84a308f-c046-4985-a4f0-deaaacddef31.mp4"   # S1 · 30s
curl -sSfL -o 02_S3_3ef54818.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_211539_3ef54818-5940-444f-85ad-61ae0a30a264.mp4"   # S3 · 20s
curl -sSfL -o 03_S4_fed12f12.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_212612_fed12f12-f8c1-4f40-8baf-fb8890ae92fb.mp4"   # S4 · 20s
curl -sSfL -o 04_S5_bdf527cd.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214435_bdf527cd-fcea-4b28-93d2-7b556490b6f5.mp4"   # S5 · 15s  ⚠ REGENERATE — placeholder only
curl -sSfL -o 05_S6_f8035ad4.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214734_f8035ad4-f4ad-48e8-a7aa-b7f7a4b27520.mp4"   # S6 · 15s
curl -sSfL -o 06_S7_deedd011.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214805_deedd011-18ca-4c9b-a25e-74f7501aaa96.mp4"   # S7 · 12s
curl -sSfL -o 07_S8_01714029.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220113_01714029-13dd-4f3b-b145-c0093fb72836.mp4"   # S8 · 15s
curl -sSfL -o 08_S9_165ab3d9.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220522_165ab3d9-6fe4-4862-b606-83605e88de9d.mp4"   # S9 · 13s
curl -sSfL -o 09_S10_1971bd66.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220735_1971bd66-4b13-468f-9a3d-f962592b2433.mp4"   # S10 · 16s
curl -sSfL -o 10_S11_328324f8.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220816_328324f8-f861-44ce-abcf-a0936131c0b7.mp4"   # S11 · 8s
curl -sSfL -o 11_S12_c9da8ff1.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221201_c9da8ff1-1106-425c-8aec-77d06e74eff6.mp4"   # S12 · 11s
curl -sSfL -o 12_S13_e4b5998b.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221449_e4b5998b-1ff3-45e8-901b-a84027c36c49.mp4"   # S13 · 11s
curl -sSfL -o 13_S14_c2e2b8db.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221613_c2e2b8db-9973-488e-aee8-0a1d3494855c.mp4"   # S14 · 11s  ⚠ REGENERATE — placeholder only
curl -sSfL -o 14_S15_aa65cc3d.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222057_aa65cc3d-fc49-44f2-8007-afc318ee379b.mp4"   # S15 · 10s
curl -sSfL -o 15_S16_e8d1b2a6.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222142_e8d1b2a6-320a-4226-aa37-a1aca9edf19b.mp4"   # S16 · 8s
curl -sSfL -o 16_S17_8c13f573.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222252_8c13f573-7a01-415f-ac20-8f1f53dcc547.mp4"   # S17 · 8s
curl -sSfL -o 17_S18_4a85d97a.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222310_4a85d97a-3368-411a-957f-1bb06442eee5.mp4"   # S18 · 8s
curl -sSfL -o 18_S19_0a4c3337.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_223552_0a4c3337-498f-49bc-8aac-2ed1c52a3019.mp4"   # S19 · 8s
curl -sSfL -o 19_S20_36e39026.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_223614_36e39026-52a3-4821-9d04-23ec1ec4aba3.mp4"   # S20 · 12s
curl -sSfL -o 20_S21_d484a959.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260914_065755_d484a959-482d-4a30-913b-fef46183be71.mp4"   # S21 · 16s
curl -sSfL -o 21_S22_4bb7a3e9.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_224106_4bb7a3e9-2341-4ce3-8e3d-a8df8f592c54.mp4"   # S22 · 12s
curl -sSfL -o 22_S23_ca08e6fd.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_224142_ca08e6fd-80f4-4b6e-b672-f00c714edce6.mp4"   # S23 · 12s

echo "picks pulled: $(ls *.mp4 | wc -l) clips"

# ---- alternates, if you want them on the bench (uncomment) ----
cd ../alternates
# curl -sSfL -o S1_7ad03129.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_174017_7ad03129-7d8d-44a3-8688-08aabfec3d64.mp4"
# curl -sSfL -o S1_3a437add.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260910_203419_3a437add-909f-469f-abe4-d4ec1ab1e8c1.mp4"
# curl -sSfL -o S1_48c4b641.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260910_203413_48c4b641-9340-43bb-a813-5e4aa2de041f.mp4"
# curl -sSfL -o S3_4874d9e4.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_211539_4874d9e4-6f43-4838-91cf-803223a44ba0.mp4"
# curl -sSfL -o S4_ec2aa3e5.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_212612_ec2aa3e5-c396-46f6-8c85-80860eb23752.mp4"
# curl -sSfL -o S4_3b4e617c.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214631_3b4e617c-1c9f-4f71-afcc-87ab125e98da.mp4"
# curl -sSfL -o S4_d4fdb764.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214631_d4fdb764-7f75-4bbd-846d-3328cd9ab6bc.mp4"
# curl -sSfL -o S5_5bb46cd9.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214435_5bb46cd9-4cc2-43d1-b581-ec8b5be6b3c7.mp4"
# curl -sSfL -o S5_21e77f5d.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_213435_21e77f5d-d864-424f-a56b-89348f9aac1c.mp4"
# curl -sSfL -o S5_959236d4.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_213435_959236d4-4ce2-45a5-9d4c-d03d7292da08.mp4"
# curl -sSfL -o S6_a89f4676.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214734_a89f4676-3e0d-4506-966d-32dce04f7ab3.mp4"
# curl -sSfL -o S7_fd089667.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_214805_fd089667-31c3-4fb8-9bbd-0929dab24597.mp4"
# curl -sSfL -o S8_ba9b30eb.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220113_ba9b30eb-8875-48da-a5d5-997722cd2c99.mp4"
# curl -sSfL -o S9_ac7a4e25.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220522_ac7a4e25-e6de-4175-bbaa-c543aa36decf.mp4"
# curl -sSfL -o S10_bab3224f.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220735_bab3224f-6ea7-4d17-a89e-36ab77b6dd0f.mp4"
# curl -sSfL -o S10_4abb698e.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220721_4abb698e-fd51-4350-a51b-80130d5c0204.mp4"
# curl -sSfL -o S10_b34943d9.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220721_b34943d9-635c-4404-9726-9b7ff6fec284.mp4"
# curl -sSfL -o S11_95326675.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_220816_95326675-0f8e-4bab-8080-da7b36076f69.mp4"
# curl -sSfL -o S12_3cc59ef0.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221201_3cc59ef0-e2f8-4589-b832-eee7dc665bdc.mp4"
# curl -sSfL -o S12_f0a995ac.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260914_045750_f0a995ac-6720-4c59-b395-e60a2760867a.mp4"
# curl -sSfL -o S12_5caa2e9f.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260914_045750_5caa2e9f-d579-4c07-a431-ce5c3d0666ad.mp4"
# curl -sSfL -o S13_416f5f35.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221449_416f5f35-9bdc-411c-9b90-76cf3e7ef448.mp4"
# curl -sSfL -o S13_4779332a.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221409_4779332a-6a05-457c-93fa-8cb4c60b1744.mp4"
# curl -sSfL -o S13_820907db.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_221409_820907db-ba74-4ae3-84be-be5dc2423239.mp4"
# curl -sSfL -o S15_194f53e7.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222057_194f53e7-a52a-4b50-92c5-82bdae6e10b2.mp4"
# curl -sSfL -o S16_70c01e2f.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222142_70c01e2f-bc7b-4399-9c31-ea2d725c1741.mp4"
# curl -sSfL -o S17_256dfbfe.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222252_256dfbfe-e18a-4b42-aefa-4962f7f901bc.mp4"
# curl -sSfL -o S18_ce8cd528.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_222310_ce8cd528-18db-48db-a1a3-b956e45e3de5.mp4"
# curl -sSfL -o S19_e8858b44.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_223552_e8858b44-44fc-4f2c-b47d-077cde893c5c.mp4"
# curl -sSfL -o S20_2ab9dfa7.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_223614_2ab9dfa7-14ca-422a-a8cc-3d401575b90f.mp4"
# curl -sSfL -o S21_25660204.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260914_065755_25660204-33bc-43b9-80aa-411a0999baeb.mp4"
# curl -sSfL -o S21_906714ac.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_223632_906714ac-f799-4add-9795-cfbdae775335.mp4"
# curl -sSfL -o S22_4896c8e3.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_224106_4896c8e3-bbd9-4162-8380-c460de8fcb0d.mp4"
# curl -sSfL -o S22_6b0d0fac.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_224040_6b0d0fac-9889-4ec4-a802-b1db7b0383b6.mp4"
# curl -sSfL -o S22_d35da4ef.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_224040_d35da4ef-22dc-4e4a-9c37-d68e234de39b.mp4"
# curl -sSfL -o S23_ae644d57.mp4 "https://d8j0ntlcm91z4.cloudfront.net/user_3GIUur2SS2F0j4FthvKoUQ8VEFn/hf_20260913_224142_ae644d57-97fe-4a84-be00-74bac3c644e0.mp4"
cd ../picks

# ---- the assembly list: cut order, with the S15 split (in/out points in seconds) ----
cat > list.txt <<'LIST'
file '01_S1_f84a308f.mp4'
file '02_S3_3ef54818.mp4'
file '03_S4_fed12f12.mp4'
file '04_S5_bdf527cd.mp4'
file '05_S6_f8035ad4.mp4'
file '06_S7_deedd011.mp4'
file '07_S8_01714029.mp4'
file '08_S9_165ab3d9.mp4'
file '09_S10_1971bd66.mp4'
file '10_S11_328324f8.mp4'
file '11_S12_c9da8ff1.mp4'
file '14_S15_aa65cc3d.mp4'
inpoint 0
outpoint 5
file '12_S13_e4b5998b.mp4'
file '13_S14_c2e2b8db.mp4'
file '14_S15_aa65cc3d.mp4'
inpoint 5
file '15_S16_e8d1b2a6.mp4'
file '16_S17_8c13f573.mp4'
file '17_S18_4a85d97a.mp4'
file '18_S19_0a4c3337.mp4'
file '19_S20_36e39026.mp4'
file '20_S21_d484a959.mp4'
file '21_S22_4bb7a3e9.mp4'
file '22_S23_ca08e6fd.mp4'
LIST

# ---- rough assembly: one 1080p-scope 24fps file (re-encoded, so mixed takes are safe) ----
if command -v ffmpeg >/dev/null; then
  ffmpeg -y -f concat -safe 0 -i list.txt -vf "scale=2560:1098:flags=lanczos,fps=24" -c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k ../matter-of-light-assembly.mp4
  echo "assembly written: matter-of-light-assembly.mp4 — add the S1 voice and NEW-2 in Resolve, or ship as is"
else echo "ffmpeg not found — clips are in ./picks in cut order; list.txt is the edit"; fi
