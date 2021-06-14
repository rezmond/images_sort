
# images_sort
Sort images by year and season.

(Temporary) Start project:
from the project folder directory run

`
    python3 start <src> <dst>
`

Run tests:

`
    pytest
`

Run tests with the coverage:

`
    pytest --cov="./core" --cov-report=html
`

Roadmap:

   - [ ] The moving process view:


        Prompt:

          > python3 start -s /src/folder/path /dst/folder/path

        The keys only for stabilisation time. <br/>
        -s, --scan      - start the scan process. <br/>
        -r, --report    - create report after move. -m parameter requires. <br/>
        -m, --move      - scans then moves. <br/>

 
        - [X] 1. Scan progress:

              Scanning:
              n /current/file/path.ext

        - [X] 2. Show report:

              Movable:            x
              Not a media:        y
              No data:            z
              =====================
              Total found:x + y + z

        - [X] 3. 

            - [X] 3.1 End, if the `-s` provided.
            - [X] 3.2 If `-m` was not provided.`

                  Do You want to move the x files [y,N]: 

        - [X] 4.
            
              The "/dst/folder/" folder does not exist.
              Do You want to create it [y/N]:
        
        - [X] 5. Move progress:

              [====>                    ] %%
              /current/file/path.ext
        - [X] 6. Create report files (hidden)
        - [X] 7. If `-v` >= 2: Show move report

              Have been moved:      x
              Already existed:      y
              Not a media:          z
              No data:              q

        - [ ] 8. If `-v` > 2:

              =======================
              Report was existed in: /path/to/src/dir/report.txt


   - [ ] May be. Add flags to skip some of step in previous section
   - [ ] Update the script help
   - [ ] Case for images without exif data, but with file name like "20200429_*.jpg"
   - [X] Introduce the `mvc` folder
   - [ ] Is the target folder needed on scanning only mode?