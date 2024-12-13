<?php

namespace PdfPseudoApp\App;

use Exception;
use PdfPseudoApp\Utils\Logger;
use PDO;
use Ramsey\Uuid\Uuid;
use Throwable;

/**
 * @brief pdf pseudo app manager
 */
class PdfPseudoApp{
    /**
     * @param array<string> $pdfFilePaths pdf file paths
     * @param string $pythonScriptPath python entities load script path
     * @param string $privateStoragePath private storage path
     * @param Logger|null $logger logger
     */
    public function __construct(
        public readonly array $pdfFilePaths,
        public readonly string $pythonScriptPath,
        public readonly string $privateStoragePath,
        public readonly ?Logger $logger = null
    ){}

    /**
     * @brief search and provide the entities data to transform
     * @return array entities data
     * @throws Exception on error
     */
    public function getEntitiesToTransform():array{
        try{
            $commands = ["python3","python"];
            $sourcePathsImplode = implode(separator: ",",array: $this->pdfFilePaths);
            $dstPaths = [];

            foreach($this->pdfFilePaths as $pdfFilePath){
                $id = Uuid::uuid4()->toString();
                $dstPaths[] = "$this->privateStoragePath$id.pdf";
            }

            $dstPathsImplode = implode(separator: ",",array: $dstPaths);

            foreach($commands as $command){
                $entitiesData = @shell_exec(command: "$command $this->pythonScriptPath $sourcePathsImplode $dstPathsImplode anonymise");

                if(!empty($entitiesData))
                    break;
            }

            $conversionResult = @json_decode(json: $entitiesData,associative: true);

            if(empty($conversionResult))
                throw new Exception(message: "Empty elements get received");

            if(!$conversionResult["success"])
                throw new Exception(message: $conversionResult["error"]);

            $result = [];
            $index = 0;

            $pdo = new PDO("mysql:host=localhost;port=3306;dbname=hackathon_2024", "root", "");
            $request = $pdo->prepare("INSERT INTO anonymisation(entities,anonymous_pdf_file_path,status) VALUES(?,?,?)");

            foreach($conversionResult["entities_map"] as $baseFile => $entitiesConfig){
                $result[$baseFile] = [
                    "entitiesConfig" => $entitiesConfig,
                    "pdfAsBlob" => @base64_encode(string:@file_get_contents(filename: $dstPaths[$index]))
                ];
                $request->execute([
                    json_encode($entitiesConfig),
                    $dstPaths[$index],
                    0
                ]);
                $index++;
            }

            return $result;
        }
        catch(Throwable $e){
            $this->logger?->log(message: $e->getMessage());

            throw new Exception(message: "Fail to treat pdf");
        }
    }

    /**
     * @brief reload
     * @param string $privateStoragePath private storage path
     * @return array
     */
    public static function reload(string $privateStoragePath,string $pythonScriptPath):array{
        $pdo = new PDO("mysql:host=localhost;port=3306;dbname=hackathon_2024", "root", "");
        $request = $pdo->prepare("SELECT * FROM anonymisation");
        $request->execute();

        $rows = $request->fetchAll(PDO::FETCH_ASSOC);

        $sourcePaths = [];
        $dstPaths = [];
        $entitiesConfig = [];

        foreach($rows as $row){
            $sourcePaths[] = $row["anonymous_pdf_file_path"];

            $id = Uuid::uuid4()->toString();
            $dstPaths[] = "$privateStoragePath$id.pdf";
            $entitiesConfig[] = $row["entities"];
        }

        $commands = ["python3","python"];
        $sourcePathsImplode = implode(separator: ",",array: $sourcePaths);
        $dstPathsImplode = implode(separator: ",",array: $dstPaths);
        $encodedElements = json_encode($entitiesConfig);

        $id = Uuid::uuid4()->toString();
        $encodedElementsPath = "$privateStoragePath$id.txt";
        @file_put_contents($encodedElementsPath, $encodedElements);

        $result = [];

        foreach($commands as $command){
            $entitiesData = @shell_exec(command: "$command $pythonScriptPath $sourcePathsImplode $dstPathsImplode reconstruct $encodedElementsPath");

            if(empty($entitiesData))
                continue;

            # load result data
            foreach($dstPaths as $index => $dstPath){
                $result[] = [
                    "entitiesConfig" => $entitiesConfig[$index],
                    "rebuildPdfAsBlob" => @base64_encode(string:@file_get_contents(filename: $dstPath)),
                    "anonymousPdfAsBlob" => @base64_encode(string:@file_get_contents(filename: $sourcePaths[$index])),
                    "id" => $rows[$index]["id"],
                    "status" => $rows[$index]["status"] == 1
                ];
                @unlink($dstPath);
            }

            break;
        }

        return $result;
    }

    /**
     * @brief check if the provided uploaded file is secure from upload datas
     * @param array $fileDatas file data from php super global $_FILES[...]
     * @param Logger|null $logger log manager
     * @return bool if secure
     */
    public static function isUploadedFileSecure(array $fileDatas,?Logger $logger = null):bool{
        try{
            foreach($fileDatas as $fileData){
                if($fileData["type"] !== "application/pdf")
                    return false;

                $fileContent = @file_get_contents(filename: $fileData["tmp_name"], context: null,length:  4);

                if($fileContent === false || !str_starts_with(haystack: $fileContent,needle:  "%PDF"))
                    return false;
            }

            return true;
        }
        catch(Throwable $e){
            $logger?->log(message: $e->getMessage());

            return false;
        }
    }
}