
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
    pytest --cov="./src" --cov-report=html
`

Roadmap:

   - [X] The moving process view:


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
              /current/file/path.ext --> /new/file/path.ext
        - [X] 6. Create report files (hidden)
        - [X] 7. If `-v` >= 2: Show move report

              Have been moved:      x
              Already existed:      y
              Not a media:          z
              No data:              q

        - [X] 8. If `-v` > 2:

              =======================
              Report was existed in: /path/to/src/dir/report.txt

   - [X] Add count of each moving group in the move report
   - [ ] Update the script help
   - [X] Case for images without exif data, but with file name like "20200429_*.jpg"
   - [X] Introduce the `mvc` folder
   - [ ] Is the target folder needed on scanning only mode?
   - [ ] Implement the "verbosity" argument validation
   - [ ] Add the glob for path processing
   - [X] Add indents to report for text-editors that can collapse sections
   - [X] If the "report.txt" already existes then create the file with new name
   - [ ] Add the "--exclued" option for exclude some files or folders from source folder
   - [ ] It might be worth getting rid of wrapping of os functions, because they are pretty stable
   - [ ] Scanning the target folder for already exists but not in supposed folder, items
