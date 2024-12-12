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
     * @param string $pdfFilePath pdf file path
     * @param string $pythonScriptPath python entities load script path
     * @param string $privateStoragePath private storage path
     * @param Logger|null $logger logger
     */
    public function __construct(
        public readonly string $pdfFilePath,
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
            $id = Uuid::uuid4()->toString();
            $pdfDstPath = "$this->privateStoragePath$id.pdf";

            foreach($commands as $command){
                $entitiesData = @shell_exec(command: "$command $this->pythonScriptPath $this->pdfFilePath $pdfDstPath");

                if(!empty($entitiesData))
                    break;
            }

            $conversionResult = @json_decode(json: $entitiesData,associative: true);

            if(empty($conversionResult))
                throw new Exception(message: "Empty elements get received");

            $pdfContent = @file_get_contents(filename: $pdfDstPath);

            if(empty($pdfContent)){
                @unlink($pdfDstPath);
                throw new Exception(message: "Fail to read the tmp pdf file");
            }

            $result = [
                "entities" => $conversionResult,
                "pdfAsBlob" => base64_encode(string: $pdfContent)
            ];

            // delete the tmp file
            @unlink($pdfDstPath);

            return $result;
        }
        catch(Throwable $e){
            $this->logger?->log(message: $e->getMessage());

            throw new Exception(message: "Fail to treat pdf");
        }
    }

    /**
     * @brief check if the provided uploaded file is secure from upload datas
     * @param array $fileData file data from php super global $_FILES[...]
     * @param Logger|null $logger log manager
     * @return bool if secure
     */
    public static function isUploadedFileSecure(array $fileData,?Logger $logger = null):bool{
        try{
            if($fileData["type"] !== "application/pdf")
                return false;

            $fileContent = @file_get_contents(filename: $fileData["tmp_name"], context: null,length:  4);

            if($fileContent === false || !str_starts_with(haystack: $fileContent,needle:  "%PDF"))
                return false;

            return true;
        }
        catch(Throwable $e){
            $logger?->log(message: $e->getMessage());

            return false;
        }
    }
}