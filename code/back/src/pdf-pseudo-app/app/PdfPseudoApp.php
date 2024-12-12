<?php

namespace PdfPseudoApp\App;

use Exception;
use PdfPseudoApp\Utils\Logger;
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

            foreach($conversionResult["entities_map"] as $baseFile => $entitiesConfig){
                $result[$baseFile] = [
                    "entitiesConfig" => $entitiesConfig,
                    "pdfAsBlob" => @base64_encode(string:@file_get_contents(filename: $dstPaths[$index]))
                ];
                $index++;
            }

            // delete the tmp file
            foreach($dstPaths as $dstPath)
                @unlink($dstPath);

            return $result;
        }
        catch(Throwable $e){
            $this->logger?->log(message: $e->getMessage());

            throw new Exception(message: "Fail to treat pdf");
        }
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